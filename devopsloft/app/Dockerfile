FROM python:3-slim

ARG ENVIRONMENT
ARG APP_PORT

COPY .env.$ENVIRONMENT /home/.env
COPY ./devopsloft/app/. /home/
COPY modules  /home/modules

RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r /home/requirements.txt

EXPOSE $APP_PORT

WORKDIR /home
ENTRYPOINT ["python3"]
CMD ["./application.py"]
