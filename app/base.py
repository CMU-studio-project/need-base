import time

from needpubsub.subscribe import subscribe_message_async


class BaseController:
    def __init__(self, project_id: str = "iitp-class-team-4"):
        self.project_id = project_id

    def eventsub(self, subscription_id: str) -> None:
        print(f"Subscribing {subscription_id}", flush=True)
        subscribe_message_async(self.project_id, subscription_id, self.sub_callback)

    def sub_callback(self, message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        t0 = time.time()

        self.handle_callback(message, **kwargs)

        t1 = time.time()
        print(
            f"Time: {t1 - t0:.3f}s | message {kwargs.get('message_id', '')} | session {kwargs.get('session_id', '')}",
            flush=True,
        )

    def handle_callback(self, message, **kwargs):
        pass
