FROM python:3.8-slim

COPY . /need
WORKDIR /need

RUN apt update

RUN pip install pip --upgrade
RUN pip install ./need-pubsub
RUN pip install -r app/collector/requirements.txt
