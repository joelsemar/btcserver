#!/bin/bash
add-apt-repository ppa:nginx/stable
apt-get -y update 
apt-get -y install nginx




cat > "/etc/nginx/sites-available/thedayexperiment.com" << EOF
server {
        #listen   80; ## listen for ipv4; this line is default and implied
        #listen   [::]:80 default ipv6only=on; ## listen for ipv6

        root /usr/share/nginx/www;
        index index.html index.htm;

        # Make site accessible from http://localhost/
        server_name localhost;

        location /static/{
           alias /var/www/tdeserver/web/static/;
        }

        location / {
            uwsgi_pass unix://opt/run/www-data/tde.sock;
            include uwsgi_params;
        }


}
EOF

sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/thedayexperiment.com /etc/nginx/sites-enabled/thedayexperiment.com
/etc/init.d/nginx start
