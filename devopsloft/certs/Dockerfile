FROM python:3

COPY ./devopsloft/certs/generateCerts.py .
COPY ./devopsloft/certs/requirements.txt .

RUN pip3 install -r ./requirements.txt

ENTRYPOINT ["python3"]
CMD ["./generateCerts.py"]