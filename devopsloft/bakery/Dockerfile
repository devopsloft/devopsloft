FROM python:3

ARG ENVIRONMENT
ARG BAKERY_PORT

COPY .env.$ENVIRONMENT /home/.env
COPY ./devopsloft/bakery/. /home/
COPY modules  /home/modules

RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r /home/requirements.txt

EXPOSE $BAKERY_PORT

WORKDIR /home
ENTRYPOINT ["python3"]
CMD ["./application.py"]
