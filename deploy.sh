#!/bin/bash

git reset --hard
git pull

chmod +x ./deploy.sh

if [ -d ./logs ]
then
  find -type f -name "*.log" -not -name "`date +%Y-%m-%d`.log" -not -empty | xargs gzip -v
else
  mkdir "logs"
fi

docker compose down
docker compose up -d
