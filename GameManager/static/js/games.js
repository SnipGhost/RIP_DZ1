var pages = true;
var page = 2;

function load_next_page() {
    pages = false;
    $.ajax({
        type: 'GET',
        url: 'page/?page=' + page.toString(),

        success: (result) => {
            $('#games').append(result);
            window.page = window.page + 1;
            pages = true;
        },

        error: (result) => {
            pages = false;
        }
    });
    window.pages = pages
    return pages
}

document.body.onload = function () {
    window.onscroll = function () {
        var scrollTop = (window.pageYOffset || document.documentElement.scrollTop) + document.documentElement.clientHeight;
        var scrollHeight = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight
        );

        if ((scrollHeight - scrollTop < 10) && window.pages) {
            load_next_page();
        }
    }
};
