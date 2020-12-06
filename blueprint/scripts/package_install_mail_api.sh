#!/bin/bash

# clone custom login repo
sudo git clone https://github.com/halsayed/calm-mail-gateway.git /opt/app
sudo chown $USER:$USER -R /opt/app

# update docker-compose file
echo 'version: "3.0"
services:
  mail_api:
    build: ./mail_gateway/.
    restart: always
    ports:
      - "80:5000"
    environment:
      - SMTP_SERVER=smtp.gmail.com
      - SMTP_USERNAME=@@{GMAIL_ADDRESS}@@
      - SMTP_PASSWORD=@@{GMAIL_PASSWORD}@@' | tee /opt/app/docker-compose.yaml

# start docker compose
cd /opt/app
docker-compose up -d
