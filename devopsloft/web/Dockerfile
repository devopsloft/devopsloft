FROM python:3 as builder

COPY ./devopsloft/web/ /
ARG WEB_PORT
ARG WEB_SECURE_PORT
ARG APP_PORT
RUN pip3 install --upgrade pip && \
    pip install -r /requirements.txt && \
    export WEB_PORT=$WEB_PORT && \
    export WEB_SECURE_PORT=$WEB_SECURE_PORT && \
    export APP_PORT=$APP_PORT && \
    j2 /nginx.conf.j2 -o /nginx.conf

FROM nginx:stable

COPY --from=builder /nginx.conf /etc/nginx/nginx.conf

ARG WEB_PORT
ARG WEB_SECURE_PORT
EXPOSE $WEB_PORT $WEB_SECURE_PORT
