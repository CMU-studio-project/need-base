from typing import Any, Dict
from jiwer import cer
from textdistance import jaro_winkler

from app.collector.test_set import TEST_SET

class DataHandler:
    def __init__(self) -> None:
        self.multi_session_dict: Dict[str, Any] = dict()

    @staticmethod
    def _chr_match(ref: str, pred: str, threshold: float = 0.2) -> bool:
        return cer(ref, pred) <= threshold
    
    @staticmethod
    def _jw_similarity(ref: str, pred: str, threshold: float = 0.8) -> bool:
        return jaro_winkler(ref, pred) >= threshold
    
    def test_match(self, source, test_instance) -> Any:
        for data_type in ["text", "phoneme"]:
            src = source[data_type]
            ref_set = test_instance[data_type]
            thres = ref_set["threshold"]
            for ref in ref_set["ref"]:
                if (self._chr_match(ref, src, threshold=thres["cer"]) or
                        self._jw_similarity(ref, src, threshold=thres["jw"])):
                    return test_instance["value"]
        return
    
    @staticmethod
    def test_map(source, test_instance) -> Any:
        return test_instance["value"][source[test_instance["key"]]]
        
    def handle(self, complete_data: Dict[str, Any]) -> Dict[str, Any]:
        # Text
        text_data = complete_data["text"]
        text = text_data["transcript"]
        
        # Sentiment
        sentiment_data = complete_data["sentiment-analysis"]
        pred_sentiment = max(sentiment_data, key=lambda x: x["score"])["label"]
        
        # Phoneme
        phoneme_data = complete_data["phoneme"]
        phoneme = phoneme_data["transcript"]
        
        test_source = {"text": text, "sentiment": pred_sentiment, "phoneme": phoneme}

        command = {
            "power": None,
            "color": None,
            "intensity": None,
        }
        
        for test_instance in TEST_SET:
            test_target = test_instance["target"]
            if command[test_target] is not None:
                continue
            
            test_type = test_instance["type"]
            if test_type == "match":
                command[test_target] = self.test_match(test_source, test_instance)
            elif test_type == "map":
                command[test_target] = self.test_map(test_source, test_instance)
            else:
                raise ValueError("Test not supported")

        return command
