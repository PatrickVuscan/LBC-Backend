#!/bin/bash

docker run --network=host -p 8080:8080 --name api -it --rm lbc-backend
