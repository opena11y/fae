$(document).ready(function() {

    var elements = document.querySelectorAll('input, select, textarea');

    for(var i = 0; i < elements.length; i++ ) {
        var e = elements[i];

        if (" button submit hidden".indexOf(e.type) > 0) continue;

        e.addEventListener('focus', function (event) { addHighlight(event, 'fae_focus');    });
        e.addEventListener('blur',  function (event) { removeHighlight(event, 'fae_focus'); });
        e.parentNode.addEventListener('mouseover', function (event) { addHighlight(event, 'fae_hover');   });
        e.parentNode.addEventListener('mouseout',  function (event) { removeHighlight(event, 'fae_hover');});

    }

    function getHighlightWidth(node) {
        var width = 0;
        var adjust_width = 18;

        var e = node.firstElementChild;

        while(e) {
            width += e.clientWidth;
            if (e.tagName === 'SELECT') adjust_width = 36;
            if ((e.tagName === 'INPUT' && (e.type === 'RADIO' || e.type === 'CHECKBOX'))) adjust_width = 20;
            e = e.nextElementSibling;
        }

        return (width + adjust_width) + "px";
    }

    function hasDisabled(node) {

        var e = node.firstElementChild;

        while(e) {
            if (e.disabled) return true;
            e = e.nextElementSibling;
        }

        return false;
    }

    function addHighlight(event, style) {
        var node = event.currentTarget;
        if (node.tagName !== 'DIV') node = node.parentNode;
        if (hasDisabled(node)) style='fae_disabled';
        node.classList.add(style);
        node.style.width = getHighlightWidth(node);  

    };

    function removeHighlight(event, style) {
        var node = event.currentTarget;
        if (node.tagName !== 'DIV') node = node.parentNode;
        if (hasDisabled(node)) style='fae_disabled';
        node.classList.remove(style);  
    };

 });
