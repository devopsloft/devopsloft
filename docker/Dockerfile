FROM ubuntu:18.04

RUN apt update \
  && apt install -y software-properties-common \
  && apt-add-repository ppa:ansible/ansible \
  && apt-get update \
  && apt-get install -y python3-pip python3-dev ansible libmysqlclient-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /

RUN pip install -r requirements.txt \
  && ansible-galaxy install -r provisioning/playbooks/requirements.yml -p \
    provisioning/playbooks/roles \
  && ansible-playbook --connection=local --inventory 127.0.0.1, \
    provisioning/playbooks/site.yml

EXPOSE 80 3306

ENTRYPOINT ["./entrypoint.sh", "127.0.0.1", "root", "12345"]
