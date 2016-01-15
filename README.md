# Functional Accessibility Evaluator, version 2.0.0
by 
[Accessible IT Group](http://disability.illinois.edu/academic-support/aitg)<br>
[Disability Resources and Educational Servcies](http://www.disability.illinois.edu)<br>
[College of Applied Health Sciences](http://www.ahs.illinois.edu)<br>
[University of Illinois at Urbana-Champaign](http://illinois.edu)<br>

## Server Requirements

* Apache2 Web Server
* Python 3.4
* Java XX

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
	     Servername  fae-self-reg-dev.disability.illinois.edu
	     ServerAlias fae-self-reg-dev.disability.illinois.edu

  Alias /static /var/www/fae2/fae-self-reg-dev/fae2/fae2/static/

  <Directory /var/www/fae2/fae-self-reg-dev/fae2/fae2/static>
    Require all granted
  </Directory>

  <Directory /var/www/fae2/fae-self-reg-dev/fae2>
    <Files wsgi.py>
     Require all granted
    </Files>
  </Directory>

  LoadModule wsgi_module modules/mod_wsgi.so 

  WSGIDaemonProcess dev-self-reg-dev.disability.illinois.edu python-path=/var/www/fae2/fae-self-reg-dev/fae2/:/var/www/fae2/virtual-en
vironments/fae2/lib/python3.4/site-packages/
  WSGIProcessGroup  dev-self-reg-dev.disability.illinois.edu
  WSGIScriptAlias / /var/www/fae2/fae-self-reg-dev/fae2/fae2/wsgi.py
</VirtualHost>
```