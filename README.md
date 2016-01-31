# Functional Accessibility Evaluator, version 2.0.0

Development is primarily supported by the [University of Illinois at Urbana-Champaign](http://illinois.edu).  The development is lead by [Accessible IT Group](http://disability.illinois.edu/academic-support/aitg) which is a unit of [Disability Resources and Educational Servcies](http://www.disability.illinois.edu) which is part fo the [College of Applied Health Sciences](http://www.ahs.illinois.edu).  Additional contributions for the [HTMLUnit](http://htmlunit.sourceforge.net/) based web site analysis engine are provided by [Administrative Information Technology Services (ATIS)](https://www.aits.uillinois.edu/) of University Administration.



## What is Functional Accessibility Evaluator (FAE)?
* FAE analyzes a website based on the requirements of the W3C Web Content Accessibility Guidelines 2.0 Single A and AA Success Criteria.
* Every rule used in FAE 2.0 references at primary WCAG 2.0 Success Criterion requirement it is based on.
* The rules support not only accessibility, but also usable web design for people with disabilities.
* The rules support accessible and usable design by enforcing the accessible coding practices and techniques of the Accessible Rich Internet Application (ARIA) 1.0 and W3C HTML5 specifications.  


## Server Requirements

* Apache2 Web Server
* Python 2.7.x
* Java 1.8

### Python Modules

* Django==1.9
* django-registration==2.0.4
* django-timezone-field==1.3
* Markdown==2.6.5
* psycopg2==2.6.1
* pytz==2015.7
* wheel==0.24.0

### Creating a <code>secrets.json</code> file

The "secrates.json" file must be created and provides:
* Security information for Django
* Information for Django to access and manage the database
* Information on on e-mail commmunications for registration and announcements.
* Place this file in the <code><em>[absolute path]</em>/fae2/fae2</code> directory

```
{
  	"FILENAME": "secrets.json",
   	"SECRET_KEY": "",
    "DEBUG": false,
    "LOGGER_LEVEL": "INFO",
   	"DATABASE_HOST": "localhost",
   	"DATABASE_PORT": "",
   	"DATABASE_NAME": "DB name",
    "DATABASE_USER": "[DB username]",
    "DATABASE_PASSWORD": "[DB password]",
    "ALLOWED_HOSTS": ["localhost"],
    "EMAIL_HOST": "[mailserver]",
    "EMAIL_PORT": 587,
    "EMAIL_USE_TLS": true,
    "EMAIL_HOST_USER": "[email]",
    "EMAIL_HOST_USER_PASSWORD": "[mail password]",
    "ACCOUNT_ACTIVATION_DAYS" : 3,
    "CONTACT_EMAIL" : "[email]"
}
```

### Apache 2.0 Configuration Notes

* MOD_WSGI must be installed and support Python3.4 (default is typically Python 2.7)
* If a version of SELINUX (e.g. Redhat, CENTOS...) is being used, remember that application level permissions must also be set to enable Apache to execute the Django application
  * Placing the django code in existing directories with the correct permssions for Apache execution
  * Using the SELINUX <code>chcon</code> command to set the application permissions of the direcorites you use for both the python code and any virtual environments that fae2 is dependent on
  * You can view application permissions of files and directories using SELINUX <code>ls -Z</code> command

#### Helpful MOD_WSGI Resources
* [Deploy a python3.4-based Django project on Centos 6.5 with mod_wsgi: doable?](http://stackoverflow.com/questions/32642937/deploy-a-python3-4-based-django-project-on-centos-6-5-with-mod-wsgi-doable)
* [How to deploy a python3 wsgi application with apache2 and debian](http://devmartin.com/blog/2015/02/How-to-deploy-a-python3-wsgi-application-with-apache2-and-debian/)
* [How To Serve Django Applications with Apache and mod_wsgi on CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7)
* [How to Run Django with mod_wsgi and Apache with a virtualenv Python environment on a Debian VPS](https://www.digitalocean.com/community/tutorials/how-to-run-django-with-mod_wsgi-and-apache-with-a-virtualenv-python-environment-on-a-debian-vps)

#### Example Configuration File
<pre>
&lt;VirtualHost *:80 >
	     Servername  fae.<em>[domain]</em>
	     ServerAlias fae.<em>[domain]</em>

  Alias /static <em>[absolute path]</em>/fae2/fae2/static/

  &lt;Directory <em>[absolute path]</em>/fae2/fae2/static>
    Require all granted
  &lt;/Directory>

  &lt;Directory <em>[absolute path]</em>/fae2>
    &lt;Files wsgi.py>
     Require all granted
    &lt;/Files>
  &lt;/Directory>

  WSGIDaemonProcess fae2 python-path=<em>[absolute path]</em>/fae2/:<em>[absolute path]</em>/virtual-en
vironments/fae2/lib/python3.4/site-packages/
  WSGIProcessGroup  fae2
  WSGIScriptAlias <em>[absolute path]</em>/fae2/fae2/wsgi.py
&lt;/VirtualHost>
</pre>

## Setting up fae directories for read/write access
* Need to create "fae2/data/" with write permissions for fae-util.py, typically "root" 
* Need to create "fae2/logs/" with write permissions for "apache" user

## SELinux Issues (e.g. CENTOS, REDHAT)

### FAE Directory Permissions
* Need to set application permissions on fae2 files to allow apache to execute the python scripts 
* Need to set application permissions on "fae2/logs" and "fae2/data" directories to allow reading and writing ([http://www.serverlab.ca/tutorials/linux/web-servers-linux/configuring-selinux-policies-for-apache-web-servers/])

### Self Registration and sendmail configuration
* Enable send mail 
  * [http://tecadmin.net/install-sendmail-server-on-centos-rhel-server/
  * [https://sachinsharm.wordpress.com/2013/08/19/setting-up-sendmail-on-centosrhel-6-3/]
  * [http://wpguru.co.uk/2015/04/how-to-open-smtp-port-587-to-send-emails-in-plesk/]
* If you are using self registration make sure you enable Apache to send emails using sendmail ([http://www.sufinawaz.com/selinux-apache-sendmail/])
* Setup e-mail on CENTOS 7 operating system ([http://www.krizna.com/centos/setup-mail-server-centos-7/])


## Operating FAE
* Must run <code>python process_evaluation_requests.py</code> to process website evaluations
* You can run multiple copies to process multiple requests at the same time 
