from typing import Optional

from needpubsub.publish import publish_message
from needpubsub.subscribe import subscribe_message_async


class MainController:
    
    def eventsub(self, subscription_id: str, timeout: Optional[int] = None) -> None:
        subscribe_message_async(subscription_id, self.sub_callback, timeout)
    
    def sub_callback(self, message: bytes, device_id: str, session_id: str, **kwargs) -> None:
        pass
    