
CREATE DATABASE IF NOT EXISTS devopsloft;

CREATE TABLE IF NOT EXISTS devopsloft.users 
(id integer NOT NULL AUTO_INCREMENT, 
 first_name varchar(100) NOT NULL,
 last_name varchar(100), 
 email VARCHAR(320) NOT NULL,
 member_type varchar(30),
 allow_receive_emails char(1),
 password varchar(100),
 password_last_change_date date,
 last_signin_failure datetime,
 member_cancelled char(1),
 PRIMARY KEY (id));
