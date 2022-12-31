#!/bin/bash

git reset --hard
git pull

docker compose down
docker compose up -d
