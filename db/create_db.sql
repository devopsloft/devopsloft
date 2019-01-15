
CREATE DATABASE IF NOT EXISTS devopsloft;

CREATE TABLE IF NOT EXISTS devopsloft.users 
(id integer NOT NULL AUTO_INCREMENT, 
 first_name varchar(100) NOT NULL,
 last_name varchar(100), 
 email VARCHAR(320) NOT NULL,
 member_type varchar(30),
 allow_receive_emails boolean,
 password varchar(100),
 password_last_change_date date,
 member_status varchar(20) comment 'values: active/blocked/cancelled/...',
 PRIMARY KEY (id));
