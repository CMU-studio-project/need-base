#!/bin/bash

PROJECT_ROOT=$(pwd)
export GOOGLE_APPLICATION_CREDENTIAL="${PROJECT_ROOT}/credentials/iitp-class-team-4-4fb491fb905a.json"
export PYTHONPATH=${PROJECT_ROOT}:${PYTHONPATH}

PROJECT_ID=${PROJECT_ID:-'iitp-class-team-4'}
TOPIC_ID=${TOPIC_ID:-'command'}
SUBSCRIPTION_ID=${SUBSCRIPTION_ID:-'collector-sub'}

python3 ${PROJECT_ROOT}/app/collector/controller.py --project_id ${PROJECT_ID} --topic_id ${TOPIC_ID} --subscription_id ${SUBSCRIPTION_ID}
