FROM mysql:5

ENV MYSQL_DATABASE devopsloft

ENV MYSQL_ROOT_PASSWORD 12345

COPY create_db.sql /docker-entrypoint-initdb.d/

EXPOSE 3306
