FROM ubuntu:20.04

ARG ENVIRONMENT

COPY project/* /home/
COPY .env.$ENVIRONMENT /home/.env
COPY docker-compose.yml /home/
COPY web_s2i /home/web_s2i/
COPY db_s2i  /home/db_s2i
COPY app_s2i  /home/app_s2i
COPY modules  /home/modules
COPY vault /home/vault

RUN apt-get update \
  && apt-get install -y curl python3-pip python3-dev libssl-dev locales \
  && curl -o /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest \
  && chmod 777 /usr/local/bin/ecs-cli \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip \
  && locale-gen en_US.UTF-8 \ 
  && pip3 install -r /home/requirements.txt \
  && mkdir -p /home/vault/config \
  && chmod 777 /home/vault \
  && curl -sSL https://get.docker.com/ | sh

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

WORKDIR /home
ENTRYPOINT ["python3"]
CMD ["./spin-docker.py"]
