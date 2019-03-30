FROM python:3

COPY . /

RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python3"]
CMD ["./application.py"]
