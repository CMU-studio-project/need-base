import os
from concurrent import futures
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.publisher.futures import Future
# from google.oauth2 import service_account
from google.auth import load_credentials_from_file
from typing import Callable

from utils import read_json, get_project_root

PROJECT_ROOT = get_project_root()
CONFIG = read_json(PROJECT_ROOT / "pubsub/config.json")
PROJECT_ID = CONFIG["project-id"]
SERVICE_ACCOUNT = str(PROJECT_ROOT / "credentials/iitp-class-team-4-4fb491fb905a.json")
# SERVICE_ACCOUNT = PROJECT_ROOT / CONFIG["service-account"]

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(SERVICE_ACCOUNT)


def publish_test():
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    # TODO(developer)
    project_id = PROJECT_ID
    topic_id = "input_speech"
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    publish_futures = []
    
    def get_callback(
        publish_future: Future, data: str
    ) -> Callable[[Future], None]:
        def callback(publish_future: Future) -> None:
            try:
                # Wait 60 seconds for the publish call to succeed.
                print(publish_future.result(timeout=60))
            except futures.TimeoutError:
                print(f"Publishing {data} timed out.")
        
        return callback
    
    with open("pubsub/sample/inspect1.wav", "rb") as f:
        data = f.read()
    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data)
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)
    
    # Wait for all the publish futures to resolve before exiting.
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
    
    print(f"Published messages with error handler to {topic_path}.")
if __name__ == "__main__":
    publish_test()
