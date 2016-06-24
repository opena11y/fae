function domTest1() {
  var titles = document.getElementsByTagName('title');
  return ("*** title *** " + titles[0].firstChild.nodeValue + "\n");
}
