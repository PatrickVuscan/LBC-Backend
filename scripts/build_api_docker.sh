#!/bin/bash

docker build --network=host -t lbc_backend -f api/Dockerfile .
