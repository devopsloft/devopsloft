FROM certbot/certbot

COPY ./devopsloft/certbot/generateCerts.py .

ENTRYPOINT ["python3"]
CMD ["./generateCerts.py"]