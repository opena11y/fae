function domTest2() {
  var links = window.document.getElementsByTagName('a');
  alert("links => " + links);
  alert("links => " + links[0]);
  return ("*** href of first link *** " + links[0]);
}
domTest1();
