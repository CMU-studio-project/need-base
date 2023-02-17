from typing import Any, Dict

from google.cloud import speech_v1p1beta1 as speech


class GoogleCloudPipeline:
    first_lang = "en-US"
    second_langs = ["ko-KR"]
    ext2encoding = {
        "wav": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "mp3": speech.RecognitionConfig.AudioEncoding.MP3,
        "flac": speech.RecognitionConfig.AudioEncoding.FLAC,
        "ogg": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        "unspecified": speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    }
    client = speech.SpeechClient()
    lang_map = {"en-us": "en-US", "ko-kr": "ko-KR"}

    def inference(self, audio: bytes, extension: str) -> Dict[str, Any]:
        encoding = self.ext2encoding.get(extension, self.ext2encoding["unspecified"])

        audio = speech.RecognitionAudio(content=audio)

        config = speech.RecognitionConfig(
            encoding=encoding,
            language_code=self.first_lang,
            alternative_language_codes=self.second_langs,
        )

        response = self.client.recognize(config=config, audio=audio)
        try:
            if response.results:
                result = response.results[0]
                alternative = result.alternatives[0]
                transcript = alternative.transcript
                confidence = alternative.confidence
                language_code = self.lang_map.get(result.language_code)
            else:
                transcript = ""
                confidence = None
                language_code = "en-US"
        except IndexError:
            transcript = ""
            confidence = None
            language_code = "en-US"

        transcript = transcript.lower()

        return {"transcript": transcript, "confidence": confidence, "language": language_code}

    def __call__(self, audio: bytes, extension: str) -> Dict[str, Any]:
        return self.inference(audio, extension)
