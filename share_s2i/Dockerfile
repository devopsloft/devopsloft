FROM python:3

COPY . /

RUN pip3 install --default-timeout=1000 -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["./events.py"]
