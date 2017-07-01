# Setting up FAE 2.0 on CENTOS7 Linux

## Disable Selinux

Disabiling SELinux will make it much easier to install and configure FAE 2.0

[Enable or Disable SELinux](https://www.centos.org/docs/5/html/5.1/Deployment_Guide/sec-sel-enable-disable.html)

## Install Git

If git is not installed, install git

```
$ yum -y install git
```

Test git version

```
$ git --version
```

## Install Apache

If Apache web server is not installed. install using the following instructions

[How to Install Apache on CentOS 7](https://www.liquidweb.com/kb/how-to-install-apache-on-centos-7/)

## Install mod_wsgi

This is a pyhon package needed for Apache to run FAE 2.0

```
$ yum -y install mod_wsgi
```

## Install Postgres database

If postggres is not installed, installusing the following instrutions

[How To Install and Use PostgreSQL on CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-centos-7)

## Install psycopg2

```
$ yum -y install python-psycopg2
```

### Create a database user

Use the createuser command to create a database user for FAE 2.0

```
$ sudo -i -u postgres
$ createuser --interactive -P fae2user
```

### Create database

Use psql shell to create a database

```
$ createdb fae2_prod -O fae2user
```

## Install Java

If Java is not installed, install the latest version of java

```
$ sudo yum install java-1.8.0-openjdk
```

If javac is not installed, install latest version:

```
$ sudo yum install java-1.8.0-openjdk-devel
```

## Create a place to put FAE 2.0 code and clone git repository 

Create a directory to put FAE 2.0 related files

```
$ cd \var\www
$ mkdir fae2
$ cd fae2
$ git clone https://github.com/opena11y/fae2.git
```

## Setup and Configure Virtual Environment for Python

* FAE 2.0 need Python 2.7.x to run
* The virtual environment is need for Apache configuration

[Hitchhicke Guide to Virtual Environments](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)

Install virtualenv via pip:

```
$ pip install virtualenv
```

Test your installation

```
$ virtualenv --version
```


Create a virtual environment for FAE 2.0

```
$ virtualenv fae2env
```

Change directory to virtual env

```
$ cd fae2env
```

Activate virtual environment

```
$ source bin/activate
```

Install required pyton packages using requirement.txt file

```
$ cp ../fae2/requirements.txt .
$ pip install -r requirements.txt
```

Install shibboleth modue using git

```
$ pip install git+https://github.com/Brown-University-Library/django-shibboleth-remoteuser.git
```

## Create a secrets.json file for configuring local version of FAE

```
$ cp 
```

## Populate database

```

```
