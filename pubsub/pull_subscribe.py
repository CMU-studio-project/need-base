from concurrent.futures import TimeoutError  # pylint: disable=redefined-builtin
import logging
import threading
import time

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber import message as sub_message

from pubsub.utils import decrypt_message, get_project_root, read_json

PROJECT_ROOT = get_project_root()
CONFIG = read_json(PROJECT_ROOT / "pubsub/config.json")
PROJECT_ID = CONFIG["project-id"]

logger = logging.getLogger("publish-log")
logger.setLevel(logging.DEBUG)


def subscribe_message(subscription_id: str, timeout: int = 10) -> None:
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, subscription_id)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=sub_callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


def sub_callback(message: sub_message.Message) -> None:
    message_data = message.data
    decrypted_message = decrypt_message(message_data)

    rec_data = {
        "message": decrypted_message,
        "message_id": message.message_id,
    }

    if message.attributes:
        rec_data.update(**message.attributes)

    thread = threading.Thread(target=run_task, kwargs=rec_data)
    thread.start()

    message.ack()


def run_task(message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
    time.sleep(3)
    print(message)

    for key, val in kwargs.items():
        print(f"{key}: {val}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--subscription_id", type=str, help="subscription ID", default="speech-gpu-server"
    )
    args = parser.parse_args()

    subscribe_message(args.subscription_id)
