FROM ubuntu:18.04

COPY . /

RUN apt-get update && \
    apt-get install -y python3-pip libmysqlclient-dev && \
    pip3 install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["./entrypoint.sh", "db", "root", "12345"]
