import json

from needpubsub.publish import publish_message
import redis

from app.base import BaseController
from app.collector.handle import DataHandler


class MessageCollector(BaseController):
    def __init__(self, project_id: str, topic_id: str) -> None:
        super(MessageCollector, self).__init__(project_id)
        self.topic_id = topic_id
        self.redis = redis.Redis(host="redis", port=6379, db=0)
        self.redis.flushdb()
        self.handler = DataHandler(self.redis)

    def handle_callback(self, message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        device_id = kwargs.get("device_id", "")
        session_id = kwargs.get("session_id", "")
        redis_key = f"{device_id}-{session_id}"
        session_data_byte = self.redis.get(redis_key)
        if session_data_byte is None:
            session_data = {"text": None, "sentiment-analysis": None, "phoneme": None}
        else:
            session_data = json.loads(session_data_byte)

        print(f"Receiving message {message!r}", flush=True)

        data_type = kwargs.get("data_type")
        if data_type is None or data_type not in session_data:
            print(f"Invalid data type {data_type}", flush=True)
            return
        session_data[data_type] = json.loads(message.decode("utf-8"))

        if all([v is not None for v in session_data.values()]):
            self.redis.delete(redis_key)
            command = self.handler.handle(session_data)
            command_bytes = json.dumps(command, ensure_ascii=False).encode("utf-8")

            topic_id = f"{self.topic_id}-{device_id}"
            print(f"Publishing {command_bytes!r} to {topic_id}", flush=True)
            
            publish_message(
                command_bytes,
                project_id=self.project_id,
                topic_id=topic_id,
                device_id=device_id,
                session_id=session_id,
            )
        else:
            self.redis.set(redis_key, json.dumps(session_data, ensure_ascii=False))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project_id", type=str, help="Google Pub/Sub Project ID")
    parser.add_argument("-s", "--subscription_id", type=str, help="Google Pub/Sub subscription ID")
    parser.add_argument("--topic_id", type=str, help="Google Pub/Sub Topic ID")
    args = parser.parse_args()

    collector = MessageCollector(args.project_id, args.topic_id)
    collector.eventsub(args.subscription_id)
