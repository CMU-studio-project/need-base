import logging

from google.cloud import pubsub_v1

from pubsub.utils import encrypt_message, get_project_root, read_json

PROJECT_ROOT = get_project_root()
CONFIG = read_json(PROJECT_ROOT / "pubsub/config.json")
PROJECT_ID = CONFIG["project-id"]

logger = logging.getLogger("publish-log")
logger.setLevel(logging.DEBUG)


def publish_message(message: bytes, topic_id: str, **kwargs) -> None:  # type: ignore[no-untyped-def]
    # Publisher
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)

    # Message encryption
    encrypted_message = encrypt_message(message)

    future = publisher.publish(topic=topic_path, data=encrypted_message, **kwargs)
    logger.debug(future.result())


if __name__ == "__main__":
    import random

    for i in range(10):
        ri = random.randint(1, 100)
        data = f"Random number {ri}"
        print(data)

        publish_message(
            data.encode("utf-8"), "input_speech", name="kyumin", organization="coddlers"
        )
