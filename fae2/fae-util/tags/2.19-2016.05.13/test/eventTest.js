function domLoop() {
  alert("domLoop");
  var items = document.getElementsByTagName("*");
  for (var i = items.length; i--;) {
    //do stuff
    alert(items[i]);
    if (items[i].getAttribute("id"))
      alert("    id=>" + items[i].getAttribute("id"));
    if (items[i].getAttribute("onclick"))
      alert("    onclick=>" + items[i].getAttribute("onclick"));
    if (items[i].getAttribute("oaa_events.has_click"))
      alert("    oaa_events.has_click=>" + items[i].getAttribute("oaa_events.has_click"));
  }
  return "done";
}

domLoop();

