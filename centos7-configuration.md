# Setting up FAE 2.0 on CENTOS7 Linux

## Disable Selinux

Disabiling SELinux will make it much easier to install and configure FAE 2.0

[Enable or Disable SELinux](https://www.centos.org/docs/5/html/5.1/Deployment_Guide/sec-sel-enable-disable.html)

## Install Apache

If Apache web server is not installed. install using the following instructions

[How to Install Apache on CentOS 7](https://www.liquidweb.com/kb/how-to-install-apache-on-centos-7/)

## Setup and Configure Virtual Environment for Python

* FAE 2.0 need Python 2.7.x to run
* The virtual environment is need for Apache configuration

[Hitchhicker Guide to Virtual Environments](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)

Install virtualenv via pip:

```
$ pip install virtualenv
```

Test your installation

```
$ virtualenv --version
```

Create a directory to put FAE 2.0 related files

```
cd \var\www
mkdir fae2
cd fae2
```

Create a virtual environment for FAE 2.0

```
virtualenv fae2env
```
