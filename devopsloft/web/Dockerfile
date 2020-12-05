FROM python:3 as builder

COPY ./devopsloft/web/ /
ARG WEB_PORT
ARG WEB_SECURE_PORT
ARG APP_PORT
ARG BAKERY_PORT
ARG SERVER_NAME
RUN pip3 install --upgrade pip && \
    pip install -r /requirements.txt && \
    export WEB_PORT=$WEB_PORT && \
    export WEB_SECURE_PORT=$WEB_SECURE_PORT && \
    export APP_PORT=$APP_PORT && \
    export SERVER_NAME=$SERVER_NAME && \
    j2 /nginx.conf.j2 -o /nginx.conf

FROM nginx:stable

COPY --from=builder /nginx.conf /etc/nginx/conf.d/nginx.conf
RUN curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "/options-ssl-nginx.conf"
RUN curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "/ssl-dhparams.pem"

ARG WEB_PORT
ARG WEB_SECURE_PORT
EXPOSE $WEB_PORT $WEB_SECURE_PORT
