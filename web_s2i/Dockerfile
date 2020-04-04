FROM python:3 as builder

COPY ./web_s2i/ /
ARG WEB_HOST_PORT
ARG WEB_HOST_SECURE_PORT
ARG APP_HOST_PORT
RUN pip3 install --upgrade pip && \
    pip install -r /requirements.txt && \
    export WEB_HOST_PORT=$WEB_HOST_PORT && \
    export WEB_HOST_SECURE_PORT=$WEB_HOST_SECURE_PORT && \
    export APP_HOST_PORT=$APP_HOST_PORT && \
    j2 /nginx.conf.j2 -o /nginx.conf

FROM nginx:stable

COPY --from=builder /nginx.conf /etc/nginx/nginx.conf
COPY ./web_s2i/*.pem /


ARG WEB_HOST_PORT
ARG WEB_HOST_SECURE_PORT
EXPOSE $WEB_HOST_PORT $WEB_HOST_SECURE_PORT
