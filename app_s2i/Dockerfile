FROM python:3

COPY . /

RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r requirements.txt

ARG APP_GUEST_PORT
EXPOSE $APP_GUEST_PORT

ENTRYPOINT ["python3"]
CMD ["./application.py"]
