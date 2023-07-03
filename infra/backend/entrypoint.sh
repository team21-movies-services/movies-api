#!/usr/bin/env bash

./infra/backend/wait-for-it.sh

if [ "$1" = "pytest" ]
then
  pytest
elif [ $ENVIRONMENT == "development" ]; then
  uvicorn run:app --host 0.0.0.0 --port 8000 --reload
else
  gunicorn run:app -b :8000 -k uvicorn.workers.UvicornWorker
fi
