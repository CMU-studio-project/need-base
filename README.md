# NEED-Coddlers
Light bulb control with spell and house sorting hat

## Installation

#### Docker setting
You need to install [docker](https://docs.docker.com/get-docker/) corresponding to your system.

#### Clone
```shell
git clone https://github.com/CMU-studio-project/need-base.git
cd need-base
git clone https://github.com/CMU-studio-project/need-pubsub.git
```

#### Tested python version
- Python3.8
- Python3.10

#### Request credentials
- To run messaging through Google Pub/Sub, you would need service account key installed
```shell
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service/account/credentials.json
```

## Running all services
In need-base directory, run:
```shell
docker compose up -d --build
```
