# Setting up FAE 2.0 on CENTOS7 Linux

All commands are assume you are logged in as `root` or are using `sudo`.

## Disable Selinux

Disabiling SELinux will make it much easier to install and configure FAE 2.0

Edit the `/etc/sysconfig/selinux` file and change the `SELINUX=enforcing` to `SELINUX=permissive`.

```
$ nano /etc/sysconfig/selinux
```

Example of updated file:

```
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#       enforcing - SELinux security policy is enforced.
#       permissive - SELinux prints warnings instead of enforcing.
#       disabled - SELinux is fully disabled.
SELINUX=permissive
# SELINUXTYPE= type of policy in use. Possible values are:
#       targeted - Only targeted network daemons are protected.
#       strict - Full SELinux protection.
SELINUXTYPE=targeted
```

Based on the resource [Enable or Disable SELinux](https://www.centos.org/docs/5/html/5.1/Deployment_Guide/sec-sel-enable-disable.html)

## Make sure yum has updated packages

First, clean-up yum:

```
sudo yum clean all
```

As a matter of best practice we’ll update our packages:

```
sudo yum -y update
```

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

### Apache Step 1: Install Apache

Installing Apache is as simple as running just one command:

```
$ sudo yum -y install httpd
```

### Apache Step 2: Allow Apache Through the Firewall

Allow the default HTTP and HTTPS port, ports 80 and 443, through firewalld:

```
$ sudo firewall-cmd --permanent --add-port=80/tcp

$ sudo firewall-cmd --permanent --add-port=443/tcp
```

And reload the firewall:

```
$ sudo firewall-cmd --reload
```

### Apache Step 3: Configure Apache to Start on Boot

And then start Apache:

```
$ sudo systemctl start httpd
```

Be sure that Apache starts at boot:

```
$ sudo systemctl enable httpd
```

To check the status of Apache:

```
$ sudo systemctl status httpd
```

To stop Apache:

```
$ sudo systemctl stop httpd
```

Based on [How to Install Apache on CentOS 7](https://www.liquidweb.com/kb/how-to-install-apache-on-centos-7/)

## Install mod_wsgi

This is a pyhon package needed for Apache to run FAE 2.0

```
$ yum -y install mod_wsgi
```

## Install Postgres database

If postggres is not installed, installusing the following instrutions

Install the postgresql-server package and the "contrib" package, that adds some additional utilities and functionality:

```
$ yum install postgresql-server postgresql-contrib
```
Accept the prompt, by responding with a y.

Now that our software is installed, we have to perform a few steps before we can use it.

Create a new PostgreSQL database cluster:

```
$ postgresql-setup initdb
```

By default, PostgreSQL does not allow password authentication. We will change that by editing its host-based authentication (HBA) configuration.

Open the HBA configuration with your favorite text editor. We will use vi:

```
$ nano /var/lib/pgsql/data/pg_hba.conf
```
Find the lines that looks like this, near the bottom of the file:
pg_hba.conf excerpt (original)

```
host    all             all             127.0.0.1/32            ident
host    all             all             ::1/128                 ident
```
Then replace "ident" with "md5", so they look like this:
pg_hba.conf excerpt (updated)

```
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

Save and exit. PostgreSQL is now configured to allow password authentication.

Now start and enable PostgreSQL:

```
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
```

PostgreSQL is now ready to be used. We can go over how it works and how it may be different from similar database management systems you may have used.


Instructions based on [How To Install and Use PostgreSQL on CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-centos-7)

### Install `psycopg2`

The `psycogp2` package is used by python to connect to the postgres database server

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
