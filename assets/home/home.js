let bridge = null;

new QWebChannel(qt.webChannelTransport, function(channel) {

    bridge = channel.objects.bridge;
    bridge.getWallpaper(function(path) {

         if (path !== "") {

             document.body.style.backgroundImage =
                 `url("file:///${path.replace(/\\/g, "/")}")`;

         }

     });

    console.log("Connected to Python!");

});


function navigate(text) {

    text = text.trim();

    if (text === "")
        return;

    if (bridge) {
        bridge.search(text);
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
