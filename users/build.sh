#!/bin/bash

sudo docker build . -t localhost:32000/users

sudo docker push localhost:32000/users
