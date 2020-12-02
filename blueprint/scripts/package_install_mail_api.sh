#!/bin/bash

# clone custom login repo
sudo git clone https://github.com/halsayed/calm-mail-gateway.git /var/app
sudo chown $USER:$USER -R /var/app

# update docker-compose file
echo 'version: "3.0"
services:
  mail_api:
    build: ./calm-mail-gateway/.
    restart: always
    ports:
      - "80:5000"
    environment:
      - SMTP_SERVER=@@{ADDRESS}@@
      - FROM_EMAIL=@@{EMAIL_ADDRESS}@@' | tee /var/app/docker-compose.yaml

# start docker compose
cd /var/app
docker-compose up -d
