#!/bin/bash

build_and_run_spinner ()
{
    echo "building spinner image"
    docker build -t spinner . > /dev/null
    docker run -t -d --name spincontainer -v /var/run/docker.sock:/var/run/docker.sock spinner
}

test_ecs_cli ()
{
    echo "test that ecs-cli installed on spinner"
    if [[ "`docker exec -it spincontainer ecs-cli --version`" =~ "ecs-cli" ]]
    then
        echo "ecs-cli installed"
    else
        echo "error ecs-cli don't installed"
        exit 1
    fi
    
}

build_and_run_spinner
test_ecs_cli
