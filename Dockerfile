FROM ubuntu:18.04

EXPOSE 5000

RUN apt-get update -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip && \
    useradd -ms /bin/bash devopsloft && \ 
    pip install virtualenv && \
    virtualenv -p python3 venv && \
    . venv/bin/activate

COPY ./requirements.txt /app/requirements.txt 

WORKDIR /app

RUN pip install -r requirements.txt 
  
USER devopsloft

COPY . /app

CMD ["python3", "application.py"]