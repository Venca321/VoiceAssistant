function reveal() {
    var reveals = document.querySelectorAll(".site-section");

    for (var i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var elementTop = reveals[i].getBoundingClientRect().top;

        if (elementTop < windowHeight - 250) {
            underline_menu(reveals[i].id)
        }
    }
}

window.addEventListener("scroll", reveal);

underlined_old = "none";
function underline_menu(you_are_in) {
    if (you_are_in == "profile") { underlined = "menu-profile"; }
    else if (you_are_in == "preferences") { underlined = "menu-preferences"; }
    else if (you_are_in == "pro") { underlined = "menu-pro"; }

    try {
        var element = document.getElementById(underlined_old);
        element.style.color = "#ffffff";
    }
    catch { }
    try {
        var element = document.getElementById(underlined);
        element.style.color = "#5a9a9f";
    }
    catch { }
    underlined_old = underlined;
}