import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from dotenv import dotenv_values
import io

config = dotenv_values("env.env")

# VIDEO_URL = "https://youtu.be/yjtxPmHdl54"
VIDEO_URL = "C:\\Users\\babal\\Downloads\\csifactory\\csifactory-business.mp4"
#st.video(VIDEO_URL, subtitles="subtitles.vtt")

video_file = open(VIDEO_URL, 'rb')
video_bytes = video_file.read()

# st.video(video_bytes)

def translateaudio(option1, option2, audio_bytes):
    
    rttext = ""
    audio_io = io.BytesIO(audio_bytes)
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    
    speechregion = config["SPEECH_REGION"]
    speechkey = config["SPEECH_KEY"]
    #speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speechkey, region=speechregion)
    speech_translation_config.speech_recognition_language="en-US"
    

    #target_language="ta"
    target_language = option1
    speech_translation_config.add_target_language(target_language)

    #audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    #audio_config = speechsdk.audio.AudioConfig(stream=audio_io)
    audio_config = speechsdk.audio.AudioConfig(filename="Call3_separated_16k_pharmacy_call.wav")
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    print("Speak into your microphone.")
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Recognized: {}".format(translation_recognition_result.text))
        print("""Translated into '{}': {}""".format(
            target_language, 
            translation_recognition_result.translations[target_language]))
        #rttext = translation_recognition_result.text
        rttext = translation_recognition_result.translations[target_language]
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        # The neural multilingual voice can speak different languages based on the input text.
        speech_config = speechsdk.SpeechConfig(subscription=speechkey, region=speechregion)
        speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
        #speech_config.speech_recognition_language='ta-IN'
        #speech_config.speech_synthesis_voice_name='ta-IN-PallaviNeural'
        #speech_config.speech_synthesis_language='ta-IN'

        speech_config.speech_recognition_language=option2
        speech_config.speech_synthesis_language=option2
        

        #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        pull_stream = speechsdk.audio.PullAudioOutputStream()
        
        # Creates a speech synthesizer using pull stream as audio output.
        stream_config = speechsdk.audio.AudioOutputConfig(stream=pull_stream)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=stream_config)

        # Get text from the console and synthesize to the default speaker.
        #print("Enter some text that you want to speak >")
        #text = input()
        
        speech_synthesis_result = speech_synthesizer.speak_text_async(rttext).get()

        #rsstream = speechsdk.AudioDataStream(speech_synthesis_result)
        rsstream = speech_synthesis_result.audio_data
        #format=speechsdk.AudioStreamWaveFormat(
        #    pcm_data_format=speechsdk.PcmDataFormat.Pcm16Bit,
        #    sample_rate_hertz=16000, channel_count=1)
        

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(rttext))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        rttext = cancellation_details.reason
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
            rttext = cancellation_details.error_details
    return rttext, rsstream


def main():
    count = 0
    col1, col2 = st.columns(2)
    status = None
    url1 = ""
    video_file = open(VIDEO_URL, 'rb')
    video_bytes = video_file.read()

    #st.video(video_bytes)
    with col1:
        option1 = st.selectbox('Input language Conversion:',
                      ('ta', 'en', 'es'))
        
        option2 = st.selectbox('Output Voice language:',
                      ('ta-IN', 'en-US', 'es-ES', 'en-IN'))
        #st.video(video_bytes)

        audio_file = open("InboundSampleRecording.mp3", "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes)

        # Upload audio file
        uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])
        
        if uploaded_file is not None:
            audio_bytes = uploaded_file.read()
            displaytext, rsstream = translateaudio(option1, option2, audio_bytes)
            st.markdown(displaytext, unsafe_allow_html=True)
            st.audio(rsstream)

        if st.button('Translate Sentence'):
            displaytext, rsstream = translateaudio(option1, option2, audio_bytes)
            count += 1
            status = "Translation done"

            st.markdown(displaytext, unsafe_allow_html=True)
            st.audio(rsstream)

if __name__ == "__main__":
    main()