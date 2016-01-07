// Update the title of the page with H1 header content
window.addEventListener('load', function() {
    var h1 = document.getElementsByTagName('h1')[0]
    window.document.title = h1.textContent + ": " + window.document.title;
});

// Functions for tabular data


var fae2TableUtils = function() {

	var util = this;

	this.addElement = function (node, tag_name, id, class_name) {

	    if (!node) return false;

	    if (typeof id         !== 'string') id = "";
	    if (typeof class_name !== 'string') class_name = "";

	    var n = document.createElement(tag_name);

	    if (n) {
    	  	n.id = id;
      	  	n.className = class_name;
      		node.appendChild(n);
    	}  

    	return n;
	};


}
