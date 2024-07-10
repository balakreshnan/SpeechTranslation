import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from dotenv import dotenv_values
import io
import os
from openai import AzureOpenAI

config = dotenv_values("env.env")

# VIDEO_URL = "https://youtu.be/yjtxPmHdl54"
VIDEO_URL = "C:\\Users\\babal\\Downloads\\csifactory\\csifactory-business.mp4"
#st.video(VIDEO_URL, subtitles="subtitles.vtt")

video_file = open(VIDEO_URL, 'rb')
video_bytes = video_file.read()

# st.video(video_bytes)

def translateaudio(option1, option2, option3, text1):
    
    rttext = ""
    engrttext = ""
    whispertext = ""
    #audio_io = io.BytesIO(audio_bytes)
    #audio_bytes.save("temp1.wav")
    #with open("temp1.wav", "wb") as f:
    #    f.write(audio_bytes)
    audio_filename = "temp1.wav"
    ssml_string = open("ssml.xml", "r").read()

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    
    speechregion = config["SPEECH_REGION"]
    speechkey = config["SPEECH_KEY"]
    #speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speechkey, region=speechregion)
    speech_translation_config.speech_recognition_language="en-US"
    

    #target_language="ta"
    target_language = option1
    speech_translation_config.add_target_language(target_language)
    #print('Audio bytes:', audio_bytes)

    # The neural multilingual voice can speak different languages based on the input text.
    speech_config = speechsdk.SpeechConfig(subscription=speechkey, region=speechregion)
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, '1500000000')
    #speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
    speech_config.speech_synthesis_voice_name=option3

    speech_config.speech_recognition_language=option2
    speech_config.speech_synthesis_language=option2    

    #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    pull_stream = speechsdk.audio.PullAudioOutputStream()
        
    # Creates a speech synthesizer using pull stream as audio output.
    stream_config = speechsdk.audio.AudioOutputConfig(stream=pull_stream)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=stream_config)
        
    #speech_synthesis_result = speech_synthesizer.speak_text_async(rttext).get()
    speech_synthesis_result = speech_synthesizer.speak_text(text1)
    #speech_synthesis_result = speech_synthesizer.speak.text(whispertext)
    #rsstream = speechsdk.AudioDataStream(speech_synthesis_result)
    rsstream = speech_synthesis_result.audio_data
    print("Audio duration: {} seconds \n".format(speech_synthesis_result.audio_duration.total_seconds()))
    #rsstream = speechsdk.AudioDataStream(speech_synthesis_result)
      

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}] \n".format(rttext))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    return rttext, rsstream, engrttext, whispertext

def main():
    count = 0
    col1, col2 = st.columns(2)
    status = None
    url1 = ""
    video_file = open(VIDEO_URL, 'rb')
    video_bytes = video_file.read()
    displaytext = None
    engrttext = None
    whispertext = None

    #st.video(video_bytes)
    with col1:
        text1 = st.text_area("Enter text to translate", """Press 0 at any time to speak with a representative. 
                Press 1 to use Vanderbilts free automated pay by phone service. 
                Press 2 for loan payoff information. 
                Press 3 for payment status. 
                Press 4 for mortgage claim information. 
                Press 7 to repeat these options.
                Our records indicate that your loan number ends in ____. 
                If this is incorrect, 
                press 2.If you have a PIN please enter it now. If you would like to create a PIN, please enter the borrowers 5 digit mailing address zip code, followed by the # key.
                The number you entered is ___. 
                If this is incorrect press 2.
                The payment due date is ___. 
                The total amount due is ___.  
                Please note that does not reflect payments that have been made today.
                To pay a different amount press 2.
                The payment of ___ will be drafted today from the account ending in ____.
                Press 1 if you wish to continue and have this payment processed. 
                Press 2 to process this payment on a different date. 
                Press 3 if you do not wish to process this payment.
                The payment has been processed and the information will be sent to your bank for drafting. Bank processing times may vary. Please allow time for this payment to clear your account. Please note that this payment will not reflect on your loan within the automated phone system until tomorrow. 
                The confirmation number is ____.
                Press 1 to repeat this information. 
                Press * to return to the previous menu.""")
        option1 = st.selectbox('Translate to Lanugage:',
                      ('ta', 'en', 'es'))
        
        option2 = st.selectbox('Output Voice language:',
                      ('ta-IN', 'en-US', 'es-ES', 'en-IN', 'es-MX', 'es-US'))
        #st.video(video_bytes)

        options3 = st.selectbox('Output Voice language:',
                      ('ta-IN-PallaviNeural', 'en-US-AvaMultilingualNeural', 'en-US-EmmaNeural', 'en-US-BrandonNeural'
                       ,'es-ES-AlvaroNeural', 'es-ES-AbrilNeural','es-MX-JorgeNeural','es-MX-DaliaNeural',
                       'en-US-AvaNeural', 'en-US-AndrewNeural', 'en-US-EmmaNeural', 'en-US-BrianNeural',
                       'en-US-JennyNeural', 'en-US-GuyNeural', 'en-US-AriaNeural', 'en-US-DavisNeural',
                       'en-US-JaneNeural', 'en-US-JasonNeural', 'en-US-SaraNeural', 'en-US-TonyNeural',
                       'en-US-NancyNeural', 'en-US-AmberNeural', 'en-US-AnaNeural', 'en-US-AshleyNeural',
                       'en-US-BrandonNeural', 'en-US-ChristopherNeural', 'en-US-CoraNeural', 'en-US-ElizabethNeural',
                       'en-US-EricNeural', 'en-US-JacobNeural', 'en-US-JennyMultilingualNeural3', 'en-US-MichelleNeural',
                       'en-US-MonicaNeural', 'en-US-RogerNeural', 'en-US-RyanMultilingualNeural3', 'en-US-SteffanNeural',
                       'en-US-AIGenerate1Neural1', 'en-US-AIGenerate2Neural1', 'en-US-AndrewMultilingualNeural3',
                       'en-US-AvaMultilingualNeural3', 'en-US-BlueNeural1', 'en-US-KaiNeural1','en-US-LunaNeural1',
                       'es-MX-DaliaNeural', 'es-MX-JorgeNeural', 'es-MX-BeatrizNeural', 'es-MX-CandelaNeural',
                       'es-MX-CarlotaNeural', 'es-MX-CecilioNeural', 'es-MX-GerardoNeural', 'es-MX-LarissaNeural',
                       'es-MX-LibertoNeural', 'es-MX-LucianoNeural', 'es-MX-MarinaNeural', 'es-MX-NuriaNeural',
                       'es-MX-PelayoNeural', 'es-MX-RenataNeural', 'es-MX-YagoNeural') 
                       )
        #audio_file = open("Call3_separated_16k_pharmacy_call.wav", "rb")  
        #audio_bytes = audio_file.read()     

        #st.audio(audio_bytes)


        if st.button('Translate Sentence'):            
            displaytext, rsstream, engrttext, whispertext = translateaudio(option1, option2, options3, text1)
            count += 1
            status = "Translation done"

            #st.markdown(displaytext, unsafe_allow_html=True)
            st.audio(rsstream)
    with col2:
        if displaytext is not None:
            st.markdown(displaytext, unsafe_allow_html=True)
        if engrttext is not None:
            st.markdown(engrttext, unsafe_allow_html=True)
        if whispertext is not None:
            st.markdown(whispertext, unsafe_allow_html=True)

if __name__ == "__main__":
    main()