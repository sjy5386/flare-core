#!/bin/bash

git reset --hard
git pull

chmod +x ./deploy.sh

docker compose down
docker compose up -d
