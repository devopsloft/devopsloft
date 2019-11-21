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
COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt
COPY .env /home/
COPY spin.py /home/
COPY createPemFiles.py /home/
COPY web_s2i /home/web_s2i/
CMD [ "/bin/bash" ]
