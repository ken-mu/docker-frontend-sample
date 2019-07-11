#!/bin/bash
set -eu

export DOCKER_IMAGE_DIGEST=$(docker pull ${DOCKER_REGISTRY_URL}/kenmu/frontend-sample | grep sha256: | sed -r "s/^.*(sha256:[0-9a-z]+).*$/\1/")
envsubst < stage.yml | kubectl apply -f -
