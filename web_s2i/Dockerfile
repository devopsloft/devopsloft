FROM python:3

COPY . /
ARG WEB_HOST_PORT
ARG WEB_HOST_SECURE_PORT
ARG APP_HOST_PORT
ARG PROD_APP_DOMAIN
RUN pip3 install --upgrade pip && \
    pip install -r /requirements.txt && \
    export WEB_HOST_PORT=$WEB_HOST_PORT && \
    export WEB_HOST_SECURE_PORT=$WEB_HOST_SECURE_PORT && \
    export APP_HOST_PORT=$APP_HOST_PORT && \
    export PROD_APP_DOMAIN=$PROD_APP_DOMAIN && \
    j2 /nginx.conf.j2 -o /nginx.conf && \
    j2 /http.conf.j2 -o /http.conf 

FROM staticfloat/nginx-certbot

COPY --from=0 /*.conf /etc/nginx/conf.d/
# COPY *.pem /

RUN rm /etc/nginx/conf.d/certbot.conf 

ARG WEB_HOST_PORT
ARG WEB_HOST_SECURE_PORT
ARG PROD_APP_DOMAIN
EXPOSE $WEB_HOST_PORT $WEB_HOST_SECURE_PORT
