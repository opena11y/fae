// Update the title of the page with H1 header content
window.addEventListener('load', function() {
    var h1 = document.getElementsByTagName('h1')[0]
    window.document.title = h1.textContent + ": " + window.document.title;
});
