#!/bin/bash
# this is test code for now until we can try it out:

#install nginx
sudo apt-get install nginx -y

# generate password file for web interface:
newPassword = mkpasswd 5 | cut -c1-6
# cd into root to avoid permissions issues when creating .htpasswd
cd ~/
sudo printf "pi:$(openssl passwd -crypt $newPassword)\n" >> .htpasswd
# this should add a second user for admin purposes. This should allow admins 
# to log in to any web app too so they can then get to the admin page
sudo printf "admin:$(openssl passwd -crypt H3rm3s)\n" >> .htpasswd
# move into nginx directory
sudo mv .htpasswd /etc/nginx/
sudo printf "admin:$(openssl passwd -crypt H3rm3s)\n" >> .htpasswd
# display the password to the screen
printf "your password for the web app is: " +$newPassword

# generate password file for admin interface:
sudo printf "admin:$(openssl passwd -crypt H3rm3s)\n" >> .htpasswdadmin
sudo mv .htpasswdadmin /etc/nginx/

# copy the nginx default config over the current default config
sudo cp ~/SunFounder_PiCar-V/digital-config/nginx/default /etc/nginx/sites-available/default
# restart for changes to take affect
sudo service nginx restart