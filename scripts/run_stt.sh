#!/bin/bash

PROJECT_ROOT=$(pwd)
export GOOGLE_APPLICATION_CREDENTIAL="${PROJECT_ROOT}/credentials/iitp-class-team-4-4fb491fb905a.json"

PROJECT_ID=${PROJECT_ID:-'iitp-class-team-4'}
TOPIC_ID=${TOPIC_ID:-'stt-text'}
SUBSCRIPTION_ID=${SUBSCRIPTION_ID:-'pi-speech-stt'}
MODEL=${MODEL:-'wav2vec2-large'}


cd "${PROJECT_ROOT}/app/stt"

python3 controller.py --project_id ${PROJECT_ID} --topic_id ${TOPIC_ID} --subscription_id ${SUBSCRIPTION_ID} --model ${MODEL}
