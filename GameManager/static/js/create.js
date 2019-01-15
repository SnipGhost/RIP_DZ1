var update_button = document.getElementById("add");
var modal = document.getElementById('myModal');
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
var form_create = document.getElementById("form_create");

btn.onclick = function (e) {
    modal.style.display = "block";
};

span.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

function getCount(parent, getChildrensChildren) {
    var relevantChildren = 0;
    var children = parent.childNodes.length;
    for (var i = 0; i < children; i++) {
        if (parent.childNodes[i].nodeType != 3) {
            if (getChildrensChildren)
                relevantChildren += getCount(parent.childNodes[i], true);
            relevantChildren++;
        }
    }
    return relevantChildren;
}

update_button.onclick = function (e) {
    e.preventDefault();

    const formData = new FormData(form_create);

    $.ajax({
        type: 'POST',
        url: '/fast_game_creation/',
        data: formData,
        processData: false,
        contentType: false,

        success: (result) => {
            modal.style.display = "none";
            $("#no_games").remove();

            var element = document.getElementById("games");

            locker = false;
            count = getCount(element, false);
            if (count % 6 == 0 && count != 6) {
                locker = true
            }

            pages = false
            do {
                pages = load_next_page();
            } while (pages);

            if (!locker) {
                $("#games").append(result);
            }

        },

        error: (result) => {
            alert('Ошибка')
        }
    });
};