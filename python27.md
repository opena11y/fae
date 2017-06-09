# Building Python2.7 with SSL Support

## Update CentOS/Redhat and install development tools

'''
  yum -y update  
  yum groupinstall -y 'development tools'  
'''

Also you need the packages below to enable SSL, bz2, zlib for Python and some utils:

'''
  yum install -y zlib-devel bzip2-devel openssl-devel xz-libs wget  
'''

## Installing Python 2.7.8 from source

Download Python and extract it

'''
  wget http://www.python.org/ftp/python/2.7.13/Python-2.7.13.tar.xz  
  xz -d Python-2.7.13.tar.xz  
  tar -xvf Python-2.7.13.tar  
'''

## Installation process

Since we already installed all the dependencies we are ready to go:

Enter the directory:

'''  
  cd Python-2.7.13
'''

### Configure for SSL Support

### Build Python
Run the configure:

'''
  ./configure --prefix=/usr/local
'''

compile and install it:

'''
  make  
  make altinstall
'''

## Checking Python version:

'''
  [root@nicetry ~]# python2.7 -V 
  Python 2.7.13  
'''