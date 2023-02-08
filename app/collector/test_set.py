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
        "text": {"ref": ["turn on", "lumos", "tarn on"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": ["oʊ mɑs", "ɔlmoʊst", "dʊ ms", "rumʊs"], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "turn off",
        "type": "match",
        "target": "power",
        "value": "off",
        "text": {"ref": ["turn off", "nox", "good bye"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": ["lʊks", "lʊksʃ", "lʊksɛ", "bʊks"], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "brighter",
        "type": "match",
        "target": "intensity",
        "value": 40,
        "text": {"ref": ["brighter", "lumos maxima"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": ["umoʊst mæksimə ɑrgju", "lums meɪks mɑʧ", "lʊmoʊs mæksəmɑpəl əpətrɪbjutj", "ðə moʊst mæksəmər"], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "darker",
        "type": "match",
        "target": "intensity",
        "value": -40,
        "text": {"ref": ["darker", "daker"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "sentiment",
        "type": "map",
        "target": "color",
        "key": "sentiment",
        "value": {
            "positive": [308, 64, 88],
            "neutral": [120, 52, 95],
            "negative": [278, 47, 89]
        }
    },
    {
        "name": "yellow",
        "type": "match",
        "target": "color",
        "value": [40, 75, 100],
        "text": {"ref": ["yellow"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
    {
        "name": "blue",
        "type": "match",
        "target": "color",
        "value": [239, 66, 97],
        "text": {"ref": ["blue"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    },
{
        "name": "red",
        "type": "match",
        "target": "color",
        "value": [356, 75, 97],
        "text": {"ref": ["red"], "threshold": {"cer": 0.2, "jw": 0.8}},
        "phoneme": {"ref": [], "threshold": {"cer": 0.2, "jw": 0.8}},
    }
]
