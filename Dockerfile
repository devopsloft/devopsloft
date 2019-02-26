FROM python:3-alpine3.9

EXPOSE 5000

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apk update && \
    apk upgrade && \
    pip install --no-cache-dir -r requirements.txt && \
    addgroup -S devopsloft && \
    adduser -S devopsloft -G devopsloft && \
    rm -rf /var/cache/apk/*

USER devopsloft

COPY . .

CMD ["python", "application.py"]