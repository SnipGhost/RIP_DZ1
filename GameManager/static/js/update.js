var update_button = document.getElementById("update");
var update_form = document.getElementById("update_form");

update_button.onclick = function () {
    update_form.classList.remove("is-hidden");
    update_button.classList.add("is-hidden");
};