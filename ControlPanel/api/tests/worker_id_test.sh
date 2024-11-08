#!/bin/bash

LOOPS=1000

for i in $(seq 1 $LOOPS)
do
    curl http://localhost:12413
    echo ""
done
