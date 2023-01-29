from typing import Any, Dict, Tuple


class ModelBase:
    def encode_text(self, text: str) -> Dict[str, Any]:
        pass

    def predict_label(self, encoded_text: Dict[str, Any]) -> Tuple[str, float]:
        pass

    def __call__(self, text: str) -> Tuple[str, float]:
        encoded_text = self.encode_text(text)  # pylint: disable=assignment-from-no-return
        prediction = self.predict_label(encoded_text)  # pylint: disable=assignment-from-no-return
        return prediction
