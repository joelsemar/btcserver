#!/bin/bash
cd /opt
wget http://projects.unbit.it/downloads/uwsgi-1.0.4.tar.gz
tar -xvf uwsgi-1.0.4.tar.gz
cd uwsgi-1.0.4
make
cp uwsgi /usr/sbin

cat > "/etc/init/tde.conf" << EOF
description "uWSGI server for The day experiment"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
exec /usr/sbin/uwsgi --socket /opt/run/www-data/tde.sock --logto /var/log/uwsgi.log --chmod-socket --module wsgi_app --pythonpath /var/www/tdeserver/wsgi/ -p 12
EOF

mkdir /opt/run
mkdir /opt/run/www-data
touch /opt/run/www-data.sock

start tde

