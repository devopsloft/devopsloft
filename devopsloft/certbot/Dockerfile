FROM certbot/certbot

ARG ENVIRONMENT

COPY .env.$ENVIRONMENT .env

COPY ./devopsloft/certbot/generateCerts.py .
COPY ./devopsloft/certbot/init-letsencrypt.py .
COPY ./devopsloft/certbot/requirements.txt  .

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "./generateCerts.py", "--server_name", "localhost" ]