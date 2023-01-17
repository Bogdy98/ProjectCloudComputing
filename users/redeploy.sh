#!/bin/bash

sudo microk8s kubectl delete deployment.apps/users
sudo microk8s kubectl apply -f ./k8s/deployment.yaml

