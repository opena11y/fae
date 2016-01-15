# Functional Accessibility Evaluator, version 2.0.0

Development Supported by 

[Accessible IT Group](http://disability.illinois.edu/academic-support/aitg)

[Disability Resources and Educational Servcies](http://www.disability.illinois.edu)

[College of Applied Health Sciences](http://www.ahs.illinois.edu)

[University of Illinois at Urbana-Champaign](http://illinois.edu)

## What is Functional Accessibility Evaluator (FAE)?
* The Functional Accessibility Evaluator (FAE) 2.0 analyzes web pages for requirements defined by the W3C Web Content Accessibility Guidelines 2.0 Single A and AA Success Criteria.
* Every rule used in FAE 2.0 references the WCAG 2.0 Success Criterion requirement it is based on.
* The rules support not only accessibility, but also usable web design for people with disabilities.
* The rules support accessible and usable design by enforcing coding practices that use of the latest accessibility technologies like the W3C Accessible Rich Internet Application (ARIA) 1.0 and W3C HTML5 Specification specification and coding techniques that support features that improve usability of web resources by people with disabilities.


## Server Requirements

* Apache2 Web Server
* Python 3.4
* Java 1.8

### Python Modules

* Django 1.9
* django-registration-redux==1.2
* django-timezone-field==1.3
* Markdown==2.6.5
* psycopg2==2.6.1
* pytz==2015.7
* wheel==0.24.0

### Apache 2.0 Configuration Notes

#### Example Configuration File
```
<VirtualHost *:80 >
	     Servername  fae.*domain*
	     ServerAlias fae.*domain*

  Alias /static */absolute path*/fae2/fae2/static/

  <Directory */absolute path*/fae2/fae2/static>
    Require all granted
  </Directory>

  <Directory */absolute path*/fae2>
    <Files wsgi.py>
     Require all granted
    </Files>
  </Directory>

  LoadModule wsgi_module modules/mod_wsgi.so 

  WSGIDaemonProcess fae2 python-path=*/absolute path*/fae2/:*/absolute path*/virtual-en
vironments/fae2/lib/python3.4/site-packages/
  WSGIProcessGroup  fae2
  WSGIScriptAlias */absolute path*/fae2/fae2/wsgi.py
</VirtualHost>
```