$(document).ready(function() {

    var elements = document.querySelectorAll('input');

    for(var i = 0; i < elements.length; i++ ) {
        var e = elements[i];

        if (" button submit".indexOf(e.type) > 0) continue;

        var className = 'fae_' + e.tagName.toLowerCase();

        var parent = e.parentNode;
        if (parent.tagName !== 'DIV') {
            var wrapper = document.createElement('div');

            // set the wrapper as child (instead of the element)
            parent.replaceChild(wrapper, e);
            // set element as child of wrapper
            wrapper.appendChild(e);
            parent = wrapper;
            parent.classList.add(className);
        }


        e.addEventListener('focus', function (event) { addHighlight(event, 'fae_focus');    });
        e.addEventListener('blur',  function (event) { removeHighlight(event, 'fae_focus'); });
        e.parentNode.addEventListener('mouseover', function (event) { addHighlight(event, 'fae_hover');   });
        e.parentNode.addEventListener('mouseout',  function (event) { removeHighlight(event, 'fae_hover');});

    }

    function getHighlightWidth(node) {
        var width = 0;

        var e = node.firstElementChild;

        while(e) {
            width += e.clientWidth;
            e = e.nextElementSibling;
        }

        console.log(node.tagName + ": " + width)

        return (width + 16) + "px";
    }

    function addHighlight(event, style) {
        var node = event.currentTarget;
        if (node.tagName !== 'DIV') node = node.parentNode;
        node.classList.add(style);
        node.style.width = getHighlightWidth(node);  

    };

    function removeHighlight(event, style) {
        var node = event.currentTarget;
        if (node.tagName !== 'DIV') node = node.parentNode;
        node.classList.remove(style);  
    };

 });
