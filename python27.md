# Building Python2.7 with SSL Support

## Update CentOS/Redhat and install development tools

```
  yum -y update  
  yum groupinstall -y 'development tools'  
```

Also you need the packages below to enable SSL, bz2, zlib for Python and some utils:

```
  yum install -y zlib-devel bzip2-devel openssl-devel xz-libs wget  
```

## Installing Python 2.7.8 from source

### Getting Python and openssl source code

Download Python and extract it

```
  wget http://www.python.org/ftp/python/2.7.13/Python-2.7.13.tar.xz  
  xz -d Python-2.7.13.tar.xz  
  tar -xvf Python-2.7.13.tar  
```

Download and install OpenSSL from source:

```
$ wget http://www.openssl.org/source/openssl-1.0.2e.tar.gz

cd openssl-1.0.2e

$ ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl

```

Note: By default openssl will be installed under /usr/local/ssl. If you do not want to mess with existing SSL installation, then install it in the '/usr/local/openssl' directory.

```
$ make
$ make test
$ make install
```

OpenSSL installation is done. Let’s us now compile Python.

### Configure Python build for SSL Support

Enter the Python Modules directory:

```  
  cd Python-2.7.13\Modules
```

Find the following lines of code in the "Setup" file:

```
# Socket module helper for SSL support; you must comment out the other
# socket line above, and possibly edit the SSL variable:
#SSL=/usr/local/ssl
#_ssl _ssl.c \
#-DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \
#-L$(SSL)/lib -lssl -lcrypto
```

Uncomment the follwing lines to include SSL support in the Python build

```
# Socket module helper for SSL support; you must comment out the other
# socket line above, and possibly edit the SSL variable:
SSL=/usr/local/openssl
_ssl _ssl.c \
-DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \
-L$(SSL)/lib -lssl -lcrypto
```

### Build Python

Since we already installed all the dependencies we are ready to go:

Go to the parent Python directory:

```
cd ..
```

Run the configure:

```
  ./configure --prefix=/usr/local
```

compile and install it:

```
  make  
  make altinstall
```

### Checking Python version:

```
  [root@nicetry ~]# python2.7 -V 
  Python 2.7.13  
```