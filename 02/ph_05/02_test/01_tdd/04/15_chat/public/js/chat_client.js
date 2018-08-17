(function () {
    if (typeof tddjs == "undefined" ||
        typeof document == "undefined" ||
        !document.getElementById || !Object.create ||
        !tddjs.namespace("chat").userFormController) {
        alert("Browser is not supported");
        return;
    }
    var chat = tddjs.chat;
    var model = {};
    var userForm = document.getElementById("userForm");
    var userController =
        Object.create(chat.userFormController);
    userController.serModel(model);
    userController.setView(userForm);

    userController.observe("user", function(user) {
        alert("Welcome, " + user);
    });
}());