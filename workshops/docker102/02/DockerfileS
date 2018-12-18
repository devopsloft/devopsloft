FROM ubuntu:18.04

RUN apt-get update -y && useradd -ms /bin/bash devopsloft

USER devopsloft

WORKDIR /app

COPY app.py .

ENV GENERIC_VAR 1234

ADD package.tar.gz .

CMD /app.py
