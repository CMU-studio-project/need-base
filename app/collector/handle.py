from typing import Any, Dict

from jiwer import cer, wer


class DataHandler:
    def __init__(self) -> None:
        self.multi_session_dict: Dict[str, Any] = dict()

    @staticmethod
    def _word_match(ref: str, pred: str, threshold: float = 0.2) -> bool:
        return wer(ref, pred) < threshold

    @staticmethod
    def _chr_match(ref: str, pred: str, threshold: float = 0.2) -> bool:
        return cer(ref, pred) < threshold

    def handle(self, complete_data: Dict[str, Any]) -> Dict[str, Any]:
        text_data = complete_data["text"]
        text = text_data["transcript"]
        sentiment_data = complete_data["sentiment-analysis"]
        pred_sentiment = max(sentiment_data, key=lambda x: x["score"])

        command = {
            "power": None,
            "color": None,
            "intensity": None,
        }
        # check turn on
        if (
            self._chr_match("turn on", text)
            or self._chr_match("lumos", text)
            or self._chr_match("tarn on", text)
        ):
            command["power"] = "on"

        # check turn off
        elif (
            self._chr_match("turn off", text)
            or self._chr_match("nox", text)
            or self._word_match("good bye", text)
        ):
            command["power"] = "off"

        elif self._chr_match("brighter", text) or self._chr_match("lumos maxima", text):
            command["intensity"] = 40

        elif self._chr_match("darker", text) or self._chr_match("daker", text):
            command["intensity"] = -40

        # check sentiment
        sentiment_label = pred_sentiment["label"]
        if sentiment_label == "positive":
            command["color"] = [308, 64, 88]
        elif sentiment_label == "neutral":
            command["color"] = [120, 52, 95]
        elif sentiment_label == "negative":
            command["color"] = [278, 47, 89]

        elif self._chr_match("yellow", text):
            command["color"] = [40, 75, 100]

        elif self._chr_match("blue", text):
            command["color"] = [239, 66, 97]

        elif self._chr_match("red", text) or self._word_match("red", text):
            command["color"] = [356, 75, 97]

        return command
