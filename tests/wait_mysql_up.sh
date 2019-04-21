#!/usr/bin/env bash
set -e
TIMEOUT=${1:-60}
while ! (docker logs db|& grep 'MySQL init process done. Ready for start up.')
do
    printf "."
    sleep 1
    let counter=$counter+1
    if [ $counter -ge ${TIMEOUT} ]
    then
        echo -e "\nFailed wating for MySQL init process, Aborting..."
        exit 1
    fi
done