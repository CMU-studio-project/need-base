from concurrent.futures import TimeoutError  # pylint: disable=redefined-builtin
import logging
import threading
from typing import Any

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

    # The subscriber pulls a specific number of messages. The actual
    # number of messages pulled may be smaller than max_messages.
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
    )

    if len(response.received_messages) == 0:
        return

    ack_ids = []
    for received_message in response.received_messages:
        print(f"Received: {received_message.message.data}.")
        ack_ids.append(received_message.ack_id)

    # Acknowledges the received messages so they will not be sent again.
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": ack_ids}
    )
    
    sub_callback(response.received_messages[0].message)

    print(
        f"Received and acknowledged {len(response.received_messages)} messages from {subscription_path}."
    )

    # streaming_pull_future = subscriber.subscribe(subscription_path, callback=sub_callback)
    # print(f"Listening for messages on {subscription_path}..")
    #
    # # Wrap subscriber in a 'with' block to automatically call close() when done.
    # with subscriber:
    #     try:
    #         # When `timeout` is not set, result() will block indefinitely,
    #         # unless an exception is encountered first.
    #         streaming_pull_future.result(timeout=timeout)
    #     except TimeoutError:
    #         streaming_pull_future.cancel()  # Trigger the shutdown.
    #         streaming_pull_future.result()  # Block until the shutdown is complete.


def sub_callback(message: Any) -> None:
    message_data = message.data
    decrypted_message = decrypt_message(message_data)

    rec_data = {
        "message": decrypted_message,
        "message_id": message.message_id,
    }

    if message.attributes:
        rec_data.update(**message.attributes)

    run_task(**rec_data)

    # message.ack()


def run_task(message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
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
