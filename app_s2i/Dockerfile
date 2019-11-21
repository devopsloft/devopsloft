FROM python:3

COPY ./app_s2i/. /



RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r requirements.txt
COPY modules /modules
COPY .env /.env
ARG APP_GUEST_PORT
EXPOSE $APP_GUEST_PORT

ENTRYPOINT ["python3"]
CMD ["./application.py"]
