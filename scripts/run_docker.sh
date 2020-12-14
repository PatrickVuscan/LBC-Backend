#!/bin/bash

docker run --network=host -p 8080:8080 --name lbc-backend -it --rm lbc-backend
