#!/usr/bin/env

rm -Rf /etc/letsencrypt/live/www.devopsloft.io
rm -Rf /etc/letsencrypt/archive/www.devopsloft.io
rm -Rf /etc/letsencrypt/renewal/www.devopsloft.io.conf
certbot certonly -n --standalone --staging --email liora@devopsloft.io -d www.devopsloft.io --rsa-key-size 4096 --agree-tos --force-renewal
