"""
Test set collection
Define test type, target command and its value.

- types
    - match: check input text/phoneme is equivalent to test set
    - map: map prediction value to command value (e.g. sentiment)
"""


TEST_SET = [
    {
        "name": "turn on",
        "type": "match",
        "target": "power",
        "value": "on",
        "text": {"ref": ["turn on", "lumos", "tarn on", "루모스", "턴온"], "threshold": {"cer": 0.2, "jw": 0.925}},
        "phoneme": {
            "ref": ["oʊ mɑs", "ɔlmoʊst", "dʊ ms", "rumʊs"],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
    },
    {
        "name": "turn off",
        "type": "match",
        "target": "power",
        "value": "off",
        "text": {"ref": ["turn off", "nox", "good bye", "녹스", "턴오프"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {
            "ref": ["lʊks", "lʊksʃ", "lʊksɛ", "bʊks"],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
    },
    {
        "name": "brightest",
        "type": "match",
        "target": "intensity",
        "value": 100,
        "text": {"ref": ["brightest", "lumos solem", "루모스 솔렘", "루모스 솔램"], "threshold": {"cer": 0.2, "jw": 0.94}},
        "phoneme": {
            "ref": [
                "lu moʊst sɑlɛnər",
                "lmoʊst soʊlɛm",
                "lumoʊstsoʊlɛmə",
                "moʊst sɔlɛm",
            ],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
    },
    {
        "name": "brighter",
        "type": "match",
        "target": "intensity",
        "value": 40,
        "text": {"ref": ["brighter", "lumos maxima", "루모스 맥시마", "브라이터"], "threshold": {"cer": 0.2, "jw": 0.87}},
        "phoneme": {
            "ref": [
                "umoʊst mæksimə ɑrgju",
                "lums meɪks mɑʧ",
                "lʊmoʊs mæksəmɑpəl əpətrɪbjutj",
                "ðə moʊst mæksəmər",
            ],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
    },
    {
        "name": "darker",
        "type": "match",
        "target": "intensity",
        "value": -40,
        "text": {"ref": ["darker", "daker", "다커"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "yellow",
        "type": "match",
        "target": "color",
        "value": [40, 75, 100],
        "text": {"ref": ["yellow", "노랑", "노란색", "옐로"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "blue",
        "type": "match",
        "target": "color",
        "value": [239, 66, 97],
        "text": {
            "ref": ["blue", "파랑", "파란색", "알로호모라", "alohomora", "블루"],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "red",
        "type": "match",
        "target": "color",
        "value": [356, 75, 97],
        "text": {"ref": ["red", "빨강", "빨간색", "레드"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "sentiment",
        "type": "map",
        "target": "color",
        "key": "sentiment",
        "value": {"positive": [86, 100, 80], "neutral": [120, 52, 95], "negative": [0, 100, 96]},
    },
]

HOUSE_TEST_SET = {
    "gryffindor": {
        "test_word": "test",
        "wav_file": "gryffindor wave file",
        "target_sentiment": "positive",
        "next": "slytherin",
    },
    "slytherin": {
        "test_word": "test",
        "wav_file": "slytherin wave file",
        "target_sentiment": "positive",
        "next": "hufflepuff",
    },
    "hufflepuff": {
        "test_word": "test",
        "wav_file": "hufflepuff wave file",
        "target_sentiment": "negative",
        "next": "ravenclaw",
    },
    "ravenclaw": {
        "test_word": "test",
        "wav_file": "ravenclaw wave file",
        "target_sentiment": "positive",
        "next": None,
    },
    "start": {
        "name": "house start",
        "type": "match",
        "target": "house",
        "value": "house",
        "text": {
            "ref": ["house test", "hogwart house test", "sort me", "하우스 테스트", "하우스테스트", "호그와트 하우스 테스트", "솔트 미", "소트 미"],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    "stop": {
        "name": "house end",
        "type": "match",
        "target": "house",
        "value": "stop",
        "text": {
            "ref": ["stop sorting", "finite", "스탑 소팅"],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
        "phoneme": {"ref": ["ɛnip"], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    "replay": {
        "name": "house replay",
        "type": "match",
        "target": "house",
        "value": "replay",
        "text": {
            "ref": ["replay", "repeat", "please repeat"],
            "threshold": {"cer": 0.2, "jw": 0.8},
        },
        "phoneme": {"ref": ["rɪpɪt"], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
}
