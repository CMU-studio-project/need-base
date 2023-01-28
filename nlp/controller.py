import json

from nlp.models import load_model
from pubsub.publish import publish_message


class NLPTaskController:
    def __init__(self, task: str = "sentiment", model: str = "roberta"):
        self.model = load_model(task, model)
        self.topic_id = task

    def predict(self, text: str) -> bytes:
        pred_label, pred_prob = self.model(text)  # (label[str], prob[float])
        pred_data = json.dumps({pred_label: pred_prob}, ensure_ascii=False)
        pred_data_bytes = pred_data.encode("utf-8")

        return pred_data_bytes

    def __call__(self, message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        message_text = message.decode("utf-8")
        prediction = self.predict(message_text)
        publish_message(prediction, self.topic_id, **kwargs)
