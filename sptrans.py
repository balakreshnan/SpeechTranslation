import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import dotenv_values

config = dotenv_values("env.env")


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speechregion = config["SPEECH_REGION"]
    speechkey = config["SPEECH_KEY"]
    #speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speechkey, region=speechregion)
    speech_translation_config.speech_recognition_language="en-US"

    target_language="ta"
    speech_translation_config.add_target_language(target_language)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    print("Speak into your microphone.")
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Recognized: {}".format(translation_recognition_result.text))
        print("""Translated into '{}': {}""".format(
            target_language, 
            translation_recognition_result.translations[target_language]))
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

#recognize_from_microphone()

# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/tts-text-stream/text_stream_sample.py

# https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-translation?tabs=windows%2Cterminal&pivots=programming-language-python

def main():
    recognize_from_microphone()

if __name__ == "__main__":
    main()