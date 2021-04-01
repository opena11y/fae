# Server Update Checklist for Updating FAE

## Stop FAE background evaluation services

1. Review the processes associated with FAE (e.g. `ps -aux | grep fae2` )
1. Kill the processes that are assocated with the instance of FAE to be updated

## Git

1.  Use `git checkout [branch name]` switch to the branch for the update (e.g. typically `master`).
1.  Verify which branch you are pulling from is the one you want
1.  Use `git pull` update the files in the local directory

## Set Virutal Evenvironment and update
1. Source [path to virtual environment]/nin/activate
1. Go to the root directory of the installation
1. Update using pip: `pip install -r requirements.txt`

## fae-util configuration

If HTMLUnit was part of the update it needs to be configured
1. Update the `classpath` file in the org\fae\util directory to point o the new version of HTMLUnit
1. Use the `build` command to update the `*.class` files
1. Delete any previous tests by deleting the `test` direcotry (e.g. `rm -Rf test`)
1. Test using `.\run -c test.properties`

## Changes to models
1. Change to the `fae2` directory with `manage.py`
1. Update model initialization `python manage.py makemigrations`
1. Update databases `python manage.py migrate`

## Changes to static files
1. Change to the `fae2` directory with `manage.py`
1. Update static files directory `python manage.py collectstatic`

## Configuration changes
1. Update `secrets.jon` file with any configuration changes.

## Restart FAE background evaluation services
1. Go the directory with the service scripts
1. Restart with the service command: `service [script file name] start`
1. Restart apache server `service httpd restart`




