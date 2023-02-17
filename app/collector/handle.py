import json
from typing import Any, Dict, List, Optional

from jiwer import cer, wer
from redis.client import Redis
from textdistance import jaro_winkler

from app.collector.test_set import HOUSE_TEST_SET, TEST_SET


class DataHandler:
    def __init__(self, redis: Redis) -> None:  # type: ignore[type-arg]
        self.redis = redis

    @staticmethod
    def _word_match(ref: str, pred: str, threshold: float = 0.2, trunc: bool = False) -> bool:
        if trunc and len(pred) > len(ref):
            pred = pred[: len(ref)]
        return wer(ref, pred) <= threshold

    @staticmethod
    def _chr_match(ref: str, pred: str, threshold: float = 0.2) -> bool:
        error_rate = cer(ref, pred)
        return error_rate <= threshold

    @staticmethod
    def _jw_similarity(ref: str, pred: str, threshold: float = 0.8) -> bool:
        similarity = jaro_winkler(ref, pred)
        return similarity >= threshold

    def test_match(self, source: Dict[str, Any], test_instance: Any) -> Any:
        for data_type in ["text", "phoneme"]:
            src = source[data_type]
            ref_set = test_instance[data_type]
            thres = ref_set["threshold"]
            for ref in ref_set["ref"]:
                chr_match = self._chr_match(ref, src, threshold=thres["cer"])
                jw_match = self._jw_similarity(ref, src, threshold=thres["jw"])
                if chr_match or jw_match:
                    print(f"[Sim-Pass] ref: {ref} | pred: {src} | thres: {thres}", flush=True)
                    return test_instance["value"]
        return

    @staticmethod
    def test_map(source: Dict[str, Any], test_instance: Any) -> Any:
        return test_instance["value"][source[test_instance["key"]]]

    def test_house(
        self,
        test_source: Dict[str, Any],
        sentiment_data: List[Dict[str, Any]],
        redis_key: str, house: Optional[str] = None
    ) -> Dict[str, Any]:
        # Start
        house_sent_bytes = self.redis.get(f"{redis_key}-house")
        if house is None or house_sent_bytes is None:
            house_sentiments = {h: None for h in ["gryffindor", "slytherin", "hufflepuff",  "ravenclaw"]}
            self.redis.set(
                f"{redis_key}-house",
                json.dumps(house_sentiments, ensure_ascii=False).encode("utf-8"),
            )
            print(f"[HOUSE TEST] begins | {redis_key}", flush=True)
            return {
                "power": None,
                "color": None,
                "intensity": None,
                "speaker": HOUSE_TEST_SET["gryffindor"]["test_word"],
                "house": "gryffindor",
            }
        
        # Restart
        if self.test_match(test_source, HOUSE_TEST_SET["replay"]):
            return {
                "power": None,
                "color": None,
                "intensity": None,
                "speaker": HOUSE_TEST_SET[house]["test_word"],
                "house": house,
            }
        
        # Stop
        if self.test_match(test_source, HOUSE_TEST_SET["stop"]):
            self.redis.delete(f"{redis_key}-house")
            return {
                "power": None,
                "color": None,
                "intensity": None,
                "speaker": "House test stop",
                "house": None,
            }

        # Sentiment analysis
        test_instance = HOUSE_TEST_SET[house]
        target_sentiment = list(
            filter(lambda x: x["label"] == test_instance["target_sentiment"], sentiment_data)  # type: ignore[arg-type]
        )[0]
        house_sentiments = json.loads(house_sent_bytes.decode("utf-8"))
        house_sentiments[house] = target_sentiment["score"]

        print(
            f"[HOUSE TEST] sentiment for {house} is {target_sentiment['score']:.3f} | {redis_key}",
            flush=True,
        )

        # Next house
        next_house = test_instance["next"]
        if next_house is not None:
            self.redis.set(
                f"{redis_key}-house",
                json.dumps(house_sentiments, ensure_ascii=False).encode("utf-8"),
            )
            return {
                "power": None,
                "color": None,
                "intensity": None,
                "speaker": HOUSE_TEST_SET[next_house]["test_word"],
                "house": next_house,
            }

        # Final decision
        else:
            self.redis.delete(f"{redis_key}-house")
            final_house = max(house_sentiments.items(), key=lambda x: x[1])[0]  # type: ignore[arg-type]

            print(f"[HOUSE TEST] Final house is {final_house} | {redis_key}", flush=True)

            return {
                "power": None,
                "color": None,
                "intensity": None,
                "speaker": house_sentiments[final_house],
                "house": final_house,
            }

    def handle(
        self, complete_data: Dict[str, Any], redis_key: str, house: Optional[str] = None
    ) -> Dict[str, Any]:
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

        command = {"power": None, "color": None, "intensity": None, "speaker": None, "house": None}

        # House test
        if house is not None:
            command = self.test_house(test_source, sentiment_data, redis_key, house)

        else:
            # Other tests
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

            # House test entry
            if self.test_match(test_source, HOUSE_TEST_SET["start"]):
                command = self.test_house(test_source, sentiment_data, redis_key)

        return command
