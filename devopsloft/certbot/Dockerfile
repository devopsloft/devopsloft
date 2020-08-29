FROM certbot/certbot

COPY ./devopsloft/certbot/generateCerts.py .
COPY ./devopsloft/certbot/init-letsencrypt.sh .

ENTRYPOINT ["./generateCerts.py"]
