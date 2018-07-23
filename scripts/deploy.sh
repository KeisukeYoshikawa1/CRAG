#!/bin/sh

BASE_DIR=$( cd $(dirname $0); cd .. ; pwd )
echo $BASE_DIR

# Setting uwsgi.ini
cat << EOF > systemd/uwsgi.ini
[uwsgi]
socket = :3031
chdir = $BASE_DIR
pythonpath = $BASE_DIR
module = shop.wsgi
pidfile = /var/run/uwsgi.pid
processes = 4
threads = 2
stats = :9191
EOF


# Setting systemd file
cat << EOF > systemd/uwsgi.service
[Unit]
Description=uWSGI service

[Service]
ExecStart=/bin/bash -c 'uwsgi --ini $BASE_DIR/systemd/uwsgi.ini'

[Install]
WantedBy=multi-user.target
EOF

# Register uwsgi.service to systemd
cd /usr/lib/systemd/system
cp $BASE_DIR/systemd/uwsgi.service uwsgi.service
systemctl enable uwsgi.service