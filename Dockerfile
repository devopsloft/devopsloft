FROM ubuntu:18.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && apt-get install libssl-dev \
  && apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
COPY requirements-docker.txt /home/
RUN pip install -r /home/requirements-docker.txt
RUN pip install docker-compose
COPY .env spin-docker.py docker-compose.yml createPemFiles.py in_docker.py /home/
COPY web_s2i /home/web_s2i/
COPY db_s2i  /home/db_s2i
COPY app_s2i  /home/app_s2i
<<<<<<< HEAD
COPY modules  /home/modules
=======
>>>>>>> 379abf1... dockerfile initial
WORKDIR /home
ENTRYPOINT [ "/bin/bash" ]
