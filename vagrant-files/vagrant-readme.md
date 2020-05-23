# Using Vagrant (and VirtualBox) for Development

I've used Vagrant before but always with Varying Vagrant Vagrants for local WordPress development.

It was fine but I didn't learn the nitty gritty of how to use/configure Vagrant because I was using a tool to help me configure it automagically.

As such, the configuration files are only semi-proven but they should still be useful enough and I'll edit this if I remember to (ADHD warning).

Anyway, the files in `./vagrant-files/` really shouldn't be part of this repo because they don't really reside within it, so to speak.

I'm on a Mac and I created a directory within my user space for the VirtualBox/Vagrant VMs.

Because I wanted an Ubuntu 18.04.4 LTS machine, I named that directory/folder 
```
ubunutu18vm
```

So the (relative?) path to it is `~/ubuntu18vm`.

Instead of refering to that folder specifically (and the path therefore being OS/distro specific), I'm going to refer to that folder as the `Vagrant_Root`

Right now, the directory structure would be `~/Vagrant_Root/vagrant-files`,
thus the path to the `Vagrantfile` would be `~/Vagrant_Root/vagrant-files/Vagrantfile` and the path to the `bootstrap.sh` file would be `~/Vagrant_Root/vagrant-files/bootstrap.sh`

But the Vagrant configuration files in `vagrant-files` won't work as expected if you leave them in their current location within this repo.

They need to be one level higher, i.e. `../`, so to make them work you'd need to:
```
cp ~/Vagrant_Root/vagrant-files/Vagrantfile ~/Vagrant_Root/Vagrantfile
cp ~/Vagrant_Root/vagrant-files/bootstrap.sh ~/Vagrant_Root/bootstrap.sh
```

---------------

Or if you were to:
```
cd ~/Vagrant_Root/vagrant-files
```
You'd then:
```
mv Vagrantfile ../

# OR

cp Vagrantfile ../
```

Additionally, you'd need to:
```
mv bootstrap.sh ../

# OR

cp bootstrap.sh ../
```

I'm sure there's some way to do all of the above in a single command but that's above my pay grade so if you know a better way to accomplish or explain those tasks, pull requests are welcome.

