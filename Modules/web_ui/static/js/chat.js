
window.onload = function () {
    const input = document.getElementById("message");
    input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            document.getElementById("submit").click();
        }
    });

    const elements = ["Server 40", "Server 39", "Server 38", "Server 37", "Server 36", "Server 35", "Server 34", "Server 33", "Server 32", "Server 31", "Server 30", "Server 29", "Server 28", "Server 27", "Server 26", "Server 25", "Server 24", "Server 23", "Server 22", "Server 21", "Server 20"]
    elements.every(element => {
        var el = document.getElementById(element);
        if (!el) { return true }
        else { typeWriter(el); }
    })
}

function typeWriter(el) {
    const textArray = el.innerHTML.split('');
    el.innerHTML = '';
    if (textArray.length < 30) {
        textArray.forEach((letter, i) => setTimeout(() => (el.innerHTML += letter), 30 * i));
    }
    else {
        textArray.forEach((letter, i) => setTimeout(() => (el.innerHTML += letter), 15 * i));
    }
}