from typing import Any, Dict
from jiwer import wer, cer

class DataHandler:
    def __init__(self):
        self.multi_session_dict = dict()
        
    @staticmethod
    def _word_match(ref: str, pred: str, threshold: float = 0.2):
        return wer(ref, pred) < threshold

    @staticmethod
    def _chr_match(ref: str, pred: str, threshold: float = 0.2):
        return cer(ref, pred) < threshold
    
    def handle(self, complete_data: Dict[str: Any]) -> Dict[str, str]:
        text = complete_data["text"]
        sentiment = complete_data["sentiment"]
        
        command = dict()
        # check turn on
        if self._chr_match("turn on", text) or self._chr_match("lumos", text):
            command["power"] = "on"
        
        # check turn off
        elif self._chr_match("turn off", text) or self._chr_match("nox", text):
            command["power"] = "off"
            
        # check sentiment
        sentiment_label = sentiment["label"]
        if sentiment_label == "positive":
            command["color"] = "blue"
        elif sentiment_label == "neutral":
            command["color"] = "green"
        elif sentiment_label == "negative":
            command["color"] = "red"
        
        return command