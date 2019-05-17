rem @echo off

if "%1"=="" (
    set env=dev
) else (
    set env=%1
)

if "%env"=="dev" (
    vagrant box update --provider virtualbox
    set port=5000
) else (
    set port=80
)

vagrant destroy -f %env%
vagrant up %env%

FOR /F "tokens=2" %%A in ('vagrant ssh-config %env% ^| findstr /r /c:"HostName"') do (
    set server_name=%%A
)

Rem Sleeping 5 seconds
set seconds=5
PING -n %seconds% 127.0.0.1 >NUL 2>&1 || PING -n %1 ::1 >NUL 2>&1

start "" http://%server_name%:%port%
