FROM python:3

ARG ENVIRONMENT
ARG APP_GUEST_PORT

COPY ./app_s2i/. /

RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r requirements.txt
COPY modules /modules
COPY .env.${ENVIRONMENT} /.env
EXPOSE $APP_GUEST_PORT

ENTRYPOINT ["python3"]
CMD ["./application.py"]
