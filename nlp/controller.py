import json

from nlp.models import load_model


class NLPTaskController:
    def __init__(self, task: str = "sentiment", model: str = "roberta"):
        self.model = load_model(task, model)

    def predict(self, text: str) -> bytes:
        pred_label, pred_prob = self.model(text)  # (label[str], prob[float])
        pred_data = json.dumps({pred_label: pred_prob}, ensure_ascii=False)
        pred_data_bytes = pred_data.encode("utf-8")

        return pred_data_bytes
