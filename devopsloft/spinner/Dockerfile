FROM ubuntu:20.04

ARG ENVIRONMENT

COPY --from=library/docker:latest /usr/local/bin/docker /usr/bin/docker
COPY --from=docker/compose:latest /usr/local/bin/docker-compose /usr/bin/docker-compose

COPY devopsloft/spinner/* /home/
COPY .env.$ENVIRONMENT /home/.env
COPY docker-compose.yml /home/
COPY modules  /home/modules

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
  && if [ "$ENVIRONMENT" != "dev" ] && [ "$ENVIRONMENT" != "ci" ]; then sed -i "/external:/d" /home/docker-compose.yml; fi

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

WORKDIR /home
ENTRYPOINT ["python3"]
CMD ["./spin-docker.py"]
