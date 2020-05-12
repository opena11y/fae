# Setting Up FAE 2.1 on Ubuntu 18.04

After significant effort and frustration trying to get this working on Debian 8, 9 or 10, I was surprised to find that **Ubuntu 18.04** LTS, code named Bionic Beaver, was ideal.

**Ubuntu 18.04** ships with **Python 3.6** and readily installs **Java8** via the built-in package manager, `apt`. (**Debian 9** ships with Python 3.5 and easily installs Java8 while **Debian 10** ships with 3.7 or 3.8 but was difficult to install Java8).

I'm currently using Ubuntu 18.04 and recommend it.

## Security and Configuration Considerations

To keep things simple and consistent I have named almost everything **fae2** (this is different from the original repo).

The database is fae2, the database user is fae2, the process-group that Apache runs as is fae2.

This is fine and dandy for testing on a localhost server (in DEBUG mode, nonetheless), and might be acceptable in production if your not very security conscious but in general you don't want to have usernames, database names or passwords that are easy to guess.

- Don't use 'postgres' for the database user and 'password' as the databse password.
- Don't use 'admin' as the username of your administrator account.
- Don't use a password for your administartor account that you have used elsewhere for anything; use a password manager and generate a unique password.
- Genrate a random, unique SECRET_KEY that is long (50 characters)

There are a couple of files that contain paths to the virtual environment and absolute server paths so make sure to read the full README.md for the strings to find and replace to make sure everything matches your setup.

## Google Cloud

I'm not new to managing Linux servers but my first attempts to get this application running were using Docker on Google Kubernetes Engine (that was overkill and I couldn't get costs lower than about $150/mo), which is why I started off with Debian.

I then tried to switch to Google Cloud Run only to realize this application isn't a good fit for that because `fae-util` needs to run as a background process until this application calls it.

After weeks struggling with Google Cloud, I realized it just wasn't ideal: I want logs to be where I expect them; I want changes I make to persist; I want to be able to use `sudo` etc.

Then I finally realized that I could just use a regular old cloud computing provider and get exactly what I wanted at a much lower cost so I abandoned Google Cloud (I'll use Kubernetes again when I need to scale but I had no clue what I was getting into when I started using it).

## Software Libraries to Install (Overkill Warning)

Because of all that, by the time I tried to install FAE on an Ubuntu VM, I was pretty burnt out and under the gun to finish. So when I tried to install something and it complained about an unmet dependency, I got a little carried away and installed everything I thought I might need, even if I wasn't sure...dev libraries, debug symbols, everything:

```
sudo apt install apache2-dev aptitude build-essential libapache2-mod-wsgi-py3 libbz2-dev libgdbm-dev liblzma-dev libncurses5-dev libpq-dev libreadline-dev libsqlite3-dev libssl-dev openjdk-8-dbg openjdk-8-source postgresql postgresql-all postgresql-contrib python3-pip python3-postgresql python3-psycopg2 python3-psycopg2-dbg software-properties-common tk-dev unzip zlib1g-dev
```

As of this writing (May 2020) Ubuntu 18.04.4 includes (or defaults to installing via `apt`):
- Apache 2.4.29 (but `apache2-dev` has to be installed via `apt`)
- Postgres 10.12
- Java 8 (`openjdk-8-jdk` version `8u252-b09-1~18.04`) also called 1.8
- Python 3.6.9
- Pip 18.x

### Upgrading Installed Software

**Pip 18.x** won't be able to find Django **2.2.12** so make sure you update pip via `python3 -m pip install --upgrade pip` that brought me up to **pip 20.1**, which will be able to find Django 2.2.12, as well as the other updated python app versions in use in the current `requirements.txt` 

Without a doubt, there's a lot of bloat, those packages install a bunch of other packages (because I didn't use the `--no-install-recommends` flag with `apt install`) but at the moment I'm only trying to get everything up an working on a VM on my local machine so I can use the debug settings and apps to make sure everything works right.

Ubuntu 18.04.4 also ships with quite a bit of software that isn't critical so keep that in mind as there are performance and security considerations.

### `mod_wsgi`, Nginx Reverse Proxy and Postgres (latest) 

I have always installed `mod_wsgi` via `apt` (listed above as `libapache2-mod-wsgi-py3`) but apparently it is simpler to install it via pip so while it is included above, it isn't needed because it is installed by pip because as is listed in `requirements.txt`.

The [Django docs recommend Nginx for serving static files](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/modwsgi/) but the version that `apt search nginx` returns is 1.14.0 (the current latest "mainline" version is 1.18.0). Similarly, the current version of Postgres is 12.2.

To upgrade to more recent versions of Nginx and Postgres, you'd need to edit the "apt sources list" and while I recommend that (I plan to use Nginx as a reverse proxy in front of Apache), I'll try to explain those steps in another document later.

## Setting Up Your Virtual Environment

At this point, I installed *virtualenv* with `pip3 install virtualenv`

While the original FAE2 repo names their virtual environment `fae2env`, this repo simply uses a virtual environment called `venv`.

Additionally, while the original repo uses the traditional Apache directory for public facing websites `/var/www`, this fork uses `/opt/fae2`.

The directory `/opt` should already exist on Ubuntu so you'll need to:

```
mkdir /opt/fae2
cd /opt/fae2
```

Just to be safe type `which python3.6` it should return `/usr/bin/python3.6`.
Then type `pwd` and make sure it returns `/opt/fae2`.

If it does you're good to go and you'll type:
```
virtualenv --python /usr/bin/python3.6 venv
source venv/bin/activate
```

You should then see something in your shell prompt, usually at the start of the command prompt line, like `(venv)`

Next you'll:
```
(venv) mkdir app
(venv) cd app
```

If you haven't cloned the repo yet and you plan to use git, you would now:
```
(venv) git clone https://github.com/ADA-First/fae2.git
```

If you have downloaded the repo (and presumably aren't using git), you'd `cd` to the location where you downloaded the zip archive and then:
```
(venv) cp fae2-master.zip /opt/fae2/app
(venv) cd /opt/fae2/app
(venv) unzip fae2-master.zip
(venv) mv fae2-master fae2
(venv) cd fae2
(venv) pwd
(venv) /opt/fae2/app/fae2
```

From there, it's time to install Django and the other Python apps into your virtual environment and you'd do that with:
```
(venv) pip install -r requirements.txt
```

Now check everything that was installed with:
```
(venv) python --version
(venv) pip --version
(venv) pip list installed
```

If everything is correct you should get at least 3.6.9 for Python, at least 20.1 for Pip and the installed software should match what's listed in `requirements.txt`

The original **README.md** file should be sufficient to explain what to do from there, however the Apache Configuration file I use is modified to match the paths described above.

## Configuring Apache (2.4)

```
<VirtualHost *:80>

  ServerName  fae2.example.com  # Replace with your domain

##If you use a real subdomain, you probably don't need a www ServerAlias
# ServerAlias www.fae2.example.com
  
  Alias /static/ /opt/fae2/app/fae2/staticroot/
  Alias /robots.txt /opt/fae2/app/fae2/staticroot/robots.txt
  Alias /favicon.ico /opt/fae2/app/fae2/staticroot/favicon.ico
  
  <Directory /opt/fae2/app/fae2/staticroot>
    Require all granted
  </Directory>

  <Directory /opt/fae2/app/fae2/fae2/fae2>
    <Files wsgi.py>
     Require all granted
    </Files>
  </Directory>
  
  WSGIScriptAlias / /opt/fae2/app/fae2/fae2/fae2/wsgi.py process-group=fae2

  WSGIProcessGroup  fae2

  WSGIDaemonProcess fae2 python-path=/opt/fae2/app/fae2/fae2/fae2:/opt/fae2/venv/lib/python3.6/site-packages

## The lines below redirect HTTP to HTTPS
## so you'll need to have that set up before uncommenting 
# RewriteEngine on
# RewriteCond %{SERVER_NAME}=fae2.example.com
# RewriteRule ^https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]

</VirtualHost>
```

## Handling Static Files

I found the static files settings and functionality quite confusing and apparently so do a lot of people but I found a [good explanation here](https://rahmonov.me/posts/django-static-files/), so I renamed things to be more obvious and added a couple new directories.

The `STATIC_ROOT` (which I named 'staticroot') should be empty!

The static files (i.e. CSS and JS assets) from your apps and those that are contained in the `STATICFILES_DIRS` will be gathered and copied into that directory when you run `python manage.py collectstatic`.

Regardless of the actual path to and name of that directory, setting the `STATIC_ROOT` to "/static/" ensure that when the assets are served they are served as if they were in `example.com/static/...`.

This is also why the Apache config file above has a line setting the `Alias` for `/static/` to the actual path to the `STATIC_ROOT`. The settings are arbitrary but they need to match so if you change one, you'll need almost certainly need to change another.
