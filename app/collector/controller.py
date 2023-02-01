from typing import Optional
import json
import redis

from needpubsub.publish import publish_message
from needpubsub.subscribe import subscribe_message_async
from handle import DataHandler


class MessageCollector:
    def __init__(self, project_id: str, topic_id: str):
        self.project_id = project_id
        self.topic_id = topic_id
        self.redis = redis.Redis(host="localhost", port=6347, db=0)
        self.redis.flushdb()
        self.handler = DataHandler()
    
    def eventsub(self, subscription_id: str, timeout: Optional[int] = None) -> None:
        subscribe_message_async(self.project_id, subscription_id, self.sub_callback, timeout)
    
    def sub_callback(self, message: bytes, device_id: str, session_id: str, data_type: str, **kwargs) -> None:
        redis_key = f"{device_id}-{session_id}"
        session_data = self.redis.get(redis_key)
        if session_data is None:
            session_data = {
                "text": None,
                "sentiment": None
            }
        else:
            session_data = json.loads(session_data)
            
        if data_type == "text":
            session_data["text"] = message.decode("utf-8")
        elif data_type == "sentiment-analysis":
            session_data["sentiment"] = json.loads(message.decode("utf-8"))
        else:
            raise ValueError("Invalid data type")
        
        if all([v is not None for v in session_data.values()]):
            self.redis.delete(redis_key)
            command = self.handler.handle(session_data)
            command_bytes = json.dumps(command, ensure_ascii=False).encode("utf-8")
            topic_id = f"{self.topic_id}-{device_id}"
            publish_message(
                command_bytes,
                project_id=self.project_id,
                topic_id=topic_id,
                device_id=device_id,
                session_id=session_id,
            )
        else:
            self.redis.set(redis_key, json.dumps(session_data, ensure_ascii=False))
