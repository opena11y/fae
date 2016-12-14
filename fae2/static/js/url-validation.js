   
    function parseURL(url) {

        var parser = document.createElement('a'),
            searchObject = {},
            queries, split, i;
        // Let the browser do the work
        parser.href = url;
        // Convert query string to object
        queries = parser.search.replace(/^\?/, '').split('&');
        for( i = 0; i < queries.length; i++ ) {
            split = queries[i].split('=');
            searchObject[split[0]] = split[1];
        }
        return {
            protocol: parser.protocol,
            host: parser.host,
            hostname: parser.hostname,
            port: parser.port,
            pathname: parser.pathname,
            search: parser.search,
            searchObject: searchObject,
            hash: parser.hash
        };
    }

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
    
      var fs = document.getElementById("id_following"); 

      if (fs)  {

        var controls = fs.getElementsByTagName("input");
        
        fs.className = "follow";      

        for(var i = 1; i < controls.length; i++) {
            var c = controls[i];           
            c.removeAttribute('disabled');
        }

      }

      var n = document.getElementById("id_input_span_sub_domains");
      if (n) n.removeAttribute('disabled');
      n = document.getElementById("id_input_span_sub_domains_label");
      if (n) n.classList.remove('disabled');

      n = document.getElementById("id_input_exclude_sub_domains");
      if (n) n.removeAttribute('disabled');
      n = document.getElementById("id_input_exclude_sub_domains_label");
      if (n) n.classList.remove('disabled');

      n = document.getElementById("id_input_include_domains");
      if (n) n.removeAttribute('disabled');
      n = document.getElementById("id_input_include_domains_label");
      if (n) n.classList.remove('disabled');
   } 

   function disableFollow() {
    
      var fs = document.getElementById("id_following");

      if (fs) {

        var controls = fs.getElementsByTagName("input");
        
        fs.className = "follow disabled"
          
        for(var i = 0; i < controls.length; i++) {
          var c = controls[i];
          if (i === 0) {
            c.setAttribute('checked','');
          }
          else {
             c.setAttribute('disabled', '');
           }
        }
      }
      else {
        // for advanced reports

      var n = document.getElementById("id_input_span_sub_domains");
      if (n) n.setAttribute('disabled','');
      n = document.getElementById("id_input_span_sub_domains_label");
      if (n) n.classList.add('disabled');

      n = document.getElementById("id_input_exclude_sub_domains");
      if (n) n.setAttribute('disabled','');
      n = document.getElementById("id_input_exclude_sub_domains_label");
      if (n) n.classList.add('disabled');

      n = document.getElementById("id_input_include_domains");
      if (n) n.setAttribute('disabled','');
      n = document.getElementById("id_input_include_domains_label");
      if (n) n.classList.add('disabled');

      }
    } 

   function enableMaxPages() {
    
      var i;
      var c;

      var mps = document.getElementById("id_max_pages");      

      controls = mps.getElementsByTagName("input");
      
      for(i = 1; i < controls.length; i++) {
        c = controls[i];     
        if (c.id.indexOf("disabled") < 0 ) {
          c.removeAttribute('disabled');
        }  
      }      

   } 

   function disableMaxPages() {
    
      var i;
      var c;

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

      if (depth1.checked) {
        disableMaxPages();
      }  
      else {
        enableMaxPages();
      }  

      var url = document.getElementById("id_input_url");

      if (url) {
        var parts = parseURL(url.value);
        var pathname = parts.pathname;

        if (pathname.length > 1) {
          pathname = pathname.slice(1);

          if (pathname.length) {
            if (pathname[pathname.length-1] === '/') {
              pathname = pathname.substring(0, pathname.length-1);
            }
          }

          if (pathname.length || depth1.checked) {
            disableFollow();
          }
          else {
            enableFollow();
          }
        }
        else {
          if (depth1.checked) {
            disableFollow();
          }
          else {
            enableFollow();
          }
        }  
      }
    };

    function checkURL() {
      enableSubmit();
      updateFollow();
    };



    function initRun () {

      enableSubmit();

      var c = document.getElementById('id_input_url');

      if (c) {
        c.addEventListener('keyup', checkURL);
        c.addEventListener('blur', checkURL);
      }
    }

window.addEventListener('load', initRun);


