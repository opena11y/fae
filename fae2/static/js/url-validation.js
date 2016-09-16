   function enableSubmit() {

     function test_url() {

       var s  = node_url.value;
       s = s.trim();
       
       return s.length > 0;
     
     }

     function test_title() {
  
       var s  = node_title.value;
       s = s.trim();
       
       return s.length > 0;
   
     }

     var node_url      = document.getElementById('id_input_url');
     var node_title    = document.getElementById('id_input_title');
     var node_submit   = document.getElementById('id_submit');

     if (test_url() && test_title()) {
        node_submit.disabled = false;
        node_submit.setAttribute('title', 'Submit form to start evaluation');     
     }
     else {
        node_submit.disabled = true;
        node_submit.setAttribute('title', 'You must enter a valid URL and a title before you can request a report');     
     }
   
   }
   
   
   function disableSubmit() {
     enableFollow();
     
     var node_submit = document.getElementById('id_submit');     
     node_submit.disabled = true;
     node_submit.setAttribute('title', 'Report request has already been sent');     
   }
   
   function enableFollow() {
    
      var i;
      var c;

      var fs = document.getElementById("id_following");   

      if (fs)  {

        var controls = fs.getElementsByTagName("input");
        
        fs.className = "follow";      

        for(i = 1; i < controls.length; i++) {
            c = controls[i];           
            c.removeAttribute('disabled');
        }

        var mps = document.getElementById("id_max_pages");      

        controls = mps.getElementsByTagName("input");
        
        for(i = 1; i < controls.length; i++) {
          c = controls[i];     
          if (c.id.indexOf("disabled") < 0 ) {
            c.removeAttribute('disabled');
          }  
        }      
      }
   } 

   function disableFollow() {
    
      var i;
      var c;

      var fs = document.getElementById("id_following");      

      var controls = fs.getElementsByTagName("input");
      
      fs.className = "follow disabled"
        
      for(i = 0; i < controls.length; i++) {
        c = controls[i];
        if (i === 0) {
          c.setAttribute('checked','');
        }
        else {
           c.setAttribute('disabled', '');
         }
      }

      var mps = document.getElementById("id_max_pages");      

      controls = mps.getElementsByTagName("input");
      
      for(i = 0; i < controls.length; i++) {
        c = controls[i];
        if (i === 0) {
          c.setAttribute('checked','');
        }
        else {
           c.setAttribute('disabled', '');
         }
      }      
    } 

   function updateFollow() {
    
      var depth1 = document.getElementById("depth_1");

      if (depth1.checked) disableFollow();
      else enableFollow();
      
    }     

window.addEventListener('load', enableSubmit);
