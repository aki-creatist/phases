TestCase("AjaxCreateTest", { // XMLHttpRequestが存在することを確かめる
    "test should return XMLHttpRequest object": function () {
        var xhr = tddjs.ajax.create();
        assertNumber(xhr.readyState);
        assert(tddjs.isHostMethod(xhr, "open"));
        assert(tddjs.isHostMethod(xhr, "send"));
        //要求ヘッダーを設定するために、以下のsetRequestHeader()が必要
        assert(tddjs.isHostMethod(xhr, "setRequestHeader"));
    }
});
