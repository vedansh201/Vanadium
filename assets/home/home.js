function navigate(text) {

    text = text.trim();

    if (text === "")
        return;

    // Looks like a website
    if (text.includes(".")) {

        if (!text.startsWith("http://") &&
            !text.startsWith("https://")) {

            text = "https://" + text;
        }

        window.location.href = text;
    }

    // Otherwise search DuckDuckGo
    else {

        window.location.href =
            "https://www.bing.com/search?q=" +
            encodeURIComponent(text);
    }
}


// Search bar
const searchBox = document.getElementById("searchBox");

searchBox.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        navigate(searchBox.value);
    }

});


// Quick links
document.getElementById("github").onclick = () => {
    navigate("github.com");
};

document.getElementById("youtube").onclick = () => {
    navigate("youtube.com");
};

document.getElementById("gmail").onclick = () => {
    navigate("mail.google.com");
};

document.getElementById("wikipedia").onclick = () => {
    navigate("wikipedia.org");
};