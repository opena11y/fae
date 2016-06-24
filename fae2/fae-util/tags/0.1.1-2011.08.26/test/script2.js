function domTest2() {
  var links = window.document.getElementsByTagName('a');
  return ("*** href of first link ***\n" + links[0].href);
}
domTest1() + domTest2() ;
