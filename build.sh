#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install
# Automatically ensures tables are prepared on your target cloud instance
pipenv run python -c "from config import app, db; app.app_context().push(); db.create_all()"
