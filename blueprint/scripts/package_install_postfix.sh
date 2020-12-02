#!/bin/bash

cat << EOF | sudo debconf-set-selections
postfix postfix/mailname string @@{DOMAIN_NAME}@@
postfix postfix/main_mailer_type string 'Internet Site'
EOF
sudo apt install -y libsasl2-modules postfix

# configure username and password from Gmail account
echo '[smtp.gmail.com]:587 @@{GMAIL_ADDRESS}@@:@@{GMAIL_PASSWORD}@@' | sudo tee /etc/postfix/sasl/sasl_passwd
sudo postmap /etc/postfix/sasl/sasl_passwd
sudo chown root:root /etc/postfix/sasl/sasl_passwd /etc/postfix/sasl/sasl_passwd.db
sudo chmod 0600 /etc/postfix/sasl/sasl_passwd /etc/postfix/sasl/sasl_passwd.db

# configure postfix to relay via Gmail
sudo sed -i 's/^mynetworks =.*/& @@{NET_WHITELIST}@@/' /etc/postfix/main.cf
sudo sed -i 's/^relayhost =.*/&[smtp.gmail.com]:587/' /etc/postfix/main.cf
echo "
smtp_sasl_auth_enable = yes
smtp_sasl_security_options = noanonymous
smtp_sasl_password_maps = hash:/etc/postfix/sasl/sasl_passwd
smtp_tls_security_level = encrypt
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
" | sudo tee -a /etc/postfix/main.cf

sudo systemctl restart postfix