#!/bin/bash

TASK_NODE_IP=192.168.254.201
TASK_NODE_PORT=12413
ERROR=0

# While less than 10 errors
while [ $ERROR -lt 10 ]; do
    # Send a request to the task node
    curl -X GET http://$TASK_NODE_IP:$TASK_NODE_PORT/status
    echo ""
    sleep 0.1

    curl -X POST http://$TASK_NODE_IP:$TASK_NODE_PORT/relay/start
    echo ""
    sleep 0.1

    curl -X GET http://$TASK_NODE_IP:$TASK_NODE_PORT/status
    echo ""
    sleep 0.1

    curl -X POST http://$TASK_NODE_IP:$TASK_NODE_PORT/relay/stop
    echo ""
    sleep 0.1

    curl -X GET http://$TASK_NODE_IP:$TASK_NODE_PORT/status
    echo ""
    sleep 0.1

    curl -X POST http://$TASK_NODE_IP:$TASK_NODE_PORT/relay/reset
    echo ""
    sleep 0.1

    sleep 2
done


