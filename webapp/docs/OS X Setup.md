# PaperChase Setup

This guide will let you deploy _PaperChase_ on a fresh Mac OS X Mavericks install.

### PaperChase user

Create a `paperchase` user on the hosting machine.

### Command line tools

Install the command line tools downloading them from the [Apple developer website](https://developer.apple.com/downloads/index.action "Apple Developer") or from XCode.

### Homebrew

Install Homebrew with the following commands

    ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
    brew doctor
    brew update
    brew install git

### Less and UglifyJS

_PaperChase_ uses _less_ for its stylesheet and we need to install it in order to let _webassets_ compile them. Before we need _node_ and _npm_

    brew install node
    
and finally we can install _less_ and _UglifyJS_

    sudo npm install -g less
    sudo npm install -g uglify-js

### MySQL

Install _MySQL_

    brew install mysql

and type
    
    ln -sfv /usr/local/opt/mysql/*.plist ~/Library/LaunchAgents
    
to have _launchd_ start _MySQL_ at login.

To avoid _MySQL_ listening on any address, after the install change the bind address to `127.0.0.1`. Basically we need to edit `~/Library/LaunchAgents/homebrew.mxcl.mysql.plist` and change the file to pass 
`--bind-address=127.0.0.1` as an argument to the _LaunchAgent_

    curl -fsSL https://gist.github.com/slottermoser/5651958/raw/homebrew.mxcl.mysql.plist -o ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
    launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
    
Run `mysql_secure_installation` and set a root password, disallow remote root login, remove the test database, and reload the privileges tables.

    mysql_secure_installation

If for some reason that wasn't in your `$PATH`, it's in the _MySQL_ keg folder, i.e. `/usr/local/Cellar/mysql/5.6.10/bin/mysql_secure_installation` (depends
 on your _MySQL_ version).

Now setup the _MySQL_ user and database:

    # Login to MySQL
    mysql -u root -p

    # Create a user for PaperChase. (change $password to a real password)
    mysql> CREATE USER 'paperchase'@'localhost' IDENTIFIED BY '$password';

    # Create the PaperChase database
    mysql> CREATE DATABASE IF NOT EXISTS `paperchase_production` DEFAULT CHARACTER SET `utf8` COLLATE `utf8_unicode_ci`;

    # Grant the paperchase user necessary permissions on the table.
    mysql> GRANT SELECT, LOCK TABLES, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON `paperchase_production`.* TO 'paperchase'@'localhost';

    # Quit the database session
    mysql> \q

    # Try connecting to the new database with the new user
    sudo -u paperchase -H mysql -u paperchase -p -D paperchase_production

Notice that I have used `paperchase` as database user for the app and `paperchase_production` as database, change them to whatever suite you best.

### Redis

Install _Redis_

    brew install redis
    ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
    
### NGINX

Install _nginx_

    brew install nginx
    ln -sfv /usr/local/opt/nginx/*.plist ~/Library/LaunchAgents
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.nginx.plist

### Setup from Fabric

The best way to deploy _PaperChase_ is using _Fabric_ from a local copy of the repository. 

In order to use the `fabfile.py` provided in the repository you need to __install Fabric and Jinja2__ globally or in a virtual environment.

##### The fabfile.py

In the `fabfile.py` in the repository main directory you will find:

* The environment variables needed to deploy the application at the top after the imports.

* The methods that defines settings specific to the deploy environment. You will have to change the `hosts` environment variable to your host settings. 

If you have followed every step of this guide you won't need to change any of the other configuration settings. If you deviated at any point make sure to update the settings in the file.

##### Deploy

To do the initial deploy of the application type

    fab vm initial_setup
    
where `vm` is the name of the method defining your host settings.

##### Update

After that if you want to update the app just type

    fab vm update_app 