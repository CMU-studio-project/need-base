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
- Kyumin - 카톡/슬랙/메일

## Publish data
```python
from pubsub.publish import publish_message

data = b"Some bytes message"
publish_message(data, "topic name", any_keyword_key="any_keyword_val")
```
For topic name, ask Kyumin



