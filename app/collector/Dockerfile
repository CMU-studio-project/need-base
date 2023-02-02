FROM python:3.8-slim

COPY ./app /need/app
COPY ./credentials /need/credentials
COPY ./need-pubsub /need/need-pubsub
COPY ./scripts /need/scripts
WORKDIR /need

RUN apt update

RUN pip install pip --upgrade
RUN pip install ./need-pubsub
RUN pip install -r app/collector/requirements.txt
