# Functional Accessibility Evaluator, version 2.0.0

Development is primarilty supported by the [University of Illinois at Urbana-Champaign](http://illinois.edu).  The development is lead by [Accessible IT Group](http://disability.illinois.edu/academic-support/aitg) which is a unit of [Disability Resources and Educational Servcies](http://www.disability.illinois.edu) which is part fo the [College of Applied Health Sciences](http://www.ahs.illinois.edu).  Additional contributions for the [HTMLUnit](http://htmlunit.sourceforge.net/) based web site analysis engine are provided by [Administrative Information Technology Services (ATIS)](https://www.aits.uillinois.edu/).



## What is Functional Accessibility Evaluator (FAE)?
* FAE analyzes a website based on the requirements of the W3C Web Content Accessibility Guidelines 2.0 Single A and AA Success Criteria.
* Every rule used in FAE 2.0 references at primary WCAG 2.0 Success Criterion requirement it is based on.
* The rules support not only accessibility, but also usable web design for people with disabilities.
* The rules support accessible and usable design by enforcing the accessible coding practices and techniques of the Accessible Rich Internet Application (ARIA) 1.0 and W3C HTML5 specifications.  


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

#### Helpful Resources
* [How To Serve Django Applications with Apache and mod_wsgi on CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7)
* [How to Run Django with mod_wsgi and Apache with a virtualenv Python environment on a Debian VPS](https://www.digitalocean.com/community/tutorials/how-to-run-django-with-mod_wsgi-and-apache-with-a-virtualenv-python-environment-on-a-debian-vps)

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