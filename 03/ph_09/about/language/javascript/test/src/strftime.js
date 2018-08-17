/**
 * フォーマットしたい文字列を受け付ける
 * 日付を表す整形済み文字列を出力する
 */

//Date.prototype上に実装
Date.prototype.strftime = (function () {
    function strftime(format) { //書式指定子を対応する値に置き換える
        var date = this;

        //String.prototype.replaceは、書式指定子にマッチする正規表現とともに使用される
        //replace関数は、与えられた指定子がDate.formatsに含まれているかどうかをチェックする
        return (format + "").replace(/%([a-zA-Z])/g, function (m, f) {
            var formatter = Date.formats && Date.formats[f];

            if (typeof formatter == "function") {
                return formatter.call(Date.formats, date);
            } else if (typeof formatter == "string") {
                return date.strftime(formatter);
            }

            return f;
        });
    }

    // 内部ヘルパー
    function zeroPad(num) {
        return (+num < 10 ? "0" : "") + num;
    }

    Date.formats = {    //ヘルパーメソッドのコレクション
        // 整形メソッド群
        d: function (date) {
            return zeroPad(date.getDate());
        },

        m: function (date) {
            return zeroPad(date.getMonth() + 1);
        },

        y: function (date) {
            return zeroPad(date.getYear() % 100);
        },

        Y: function (date) {
            return date.getFullYear();
        },

        j: function (date) {
            var jan1 = new Date(date.getFullYear(), 0, 1);
            var diff = date.getTime() - jan1.getTime();

            // 86400000 == 60 * 60 * 24 * 1000
            return Math.ceil(diff / 86400000);
        },

        // フォーマット略記法
        F: "%Y-%m-%d",
        D: "%m/%d/%y"
    };

    return strftime;
}());
