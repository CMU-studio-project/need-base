# NEED-Coddlers

## Initial Setting

#### Clone
```shell
git clone https://github.com/CMU-studio-project/need-base.git
```

#### Install requirements (Under preferred env/virtualenv)
```shell
pip install -r requirements.txt
```

#### Tested version
- Python3.8
- Python3.10

#### Request credentials
- Notion 참조

## Publish data
```python
from pubsub.publish import publish_message

data = b"Some bytes message"
publish_message(data, "topic name", any_keyword_key="any_keyword_val")
```

## Run push subscription
set module/task/model
```shell
export NEED_PROJECT_MODULE=nlp
export NEED_PROJECT_TASK=sentiment
export NEED_PROJECT_MODEL=roberta
```
run eventsub server
```shell
python pubsub/push_subscribe.py
```
run ngrok
```shell
ngrok http 18080
```