FROM python:3.8-slim

COPY . /need
WORKDIR /need

RUN pip install pip --upgrade
RUN pip install ./need-pubsub
RUN pip install -r requirements.txt
