#!/bin/bash

PROJECT_ROOT=$(pwd)
export GOOGLE_APPLICATION_CREDENTIAL="${PROJECT_ROOT}/credentials/iitp-class-team-4-4fb491fb905a.json"

PROJECT_ID=${PROJECT_ID:-'iitp-class-team-4'}
TOPIC_ID=${TOPIC_ID:-'command'}
SUBSCRIPTION_ID=${SUBSCRIPTION_ID:-'collector-sub'}
TASK=${TASK:-'sentiment-analysis'}
MODEL=${MODEL:-'roberta'}


cd "${PROJECT_ROOT}/app/nlp"

python controller.py --project_id ${PROJECT_ID} --topic_id ${TOPIC_ID} --subscription_id ${SUBSCRIPTION_ID} --task ${TASK} --model ${MODEL}
