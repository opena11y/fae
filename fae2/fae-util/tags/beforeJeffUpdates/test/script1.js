function domTest1() {
  var titles = document.getElementsByTagName('title');
  return ("*** title ***\n" + titles[0].firstChild.nodeValue + "\n");
}
