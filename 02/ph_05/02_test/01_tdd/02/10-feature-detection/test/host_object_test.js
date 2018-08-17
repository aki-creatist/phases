TestCase("HostObjectTest", {
    "test IE host object behavior": function () { //フレンドリではないホストオブジェクトのふるまい
        var xhr = new ActiveXObject("Microsoft.XMLHTTP");
        assertException(function () {
            if (xhr.open) {
                // 期待：プロパティはある
                // 実際：例外が投げられる
            }
        });
        assertEquals("unknown", typeof xhr.open);
        var element = document.createElement("div");
        assertEquals("unknown", typeof element.offsetParent);
        assertException(function () {
            var parent = element.offsetParent;
        });
    }
});
