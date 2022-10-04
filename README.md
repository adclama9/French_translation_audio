# English to French translation + audio

I made this to help me learn to read/speak french. Also to play with transformers from HuggingFace ^_^

#note: Unfortunately does not run on HuggingFace space as they do not have espeak installed.

Python script that creates an interactable Gradio demo of a translator.

![image](https://user-images.githubusercontent.com/57018666/193949131-ad35858e-7e4e-4b45-b94c-07087422f696.png)

![image](https://user-images.githubusercontent.com/57018666/193949063-4f76eb80-1478-4ac4-817d-f1a04690a4f3.png)

It takes an english audio input from the user's mic and returns 3 outputs.

1. Transcribed English text
2. Translated French text
3. Text to Speech French 

## Method:
For english transcription, used OpenAi's new Whisper model (openai/whisper-medium) (Scary accurate!!!) 
Tried Facebook's wav2vec2 but whisper performs much better.

For en to fr translation, used Helsinki's Opus (Helsinki-NLP/opus-mt-en-fr). 
It performs better than Google's t5 because it's oriented to one language while t5 does multiple languages.

For text to speech (TTS), used Facebook's tts transformer (facebook/tts_transformer-fr-cv7_css10)
Strong tts tailored to french, making it perform well.


## Dependencies you have to install to run this

-requirements.txt\
-ffmpeg\
-e-speak & espean-ng\
instructions\
vvvvvvvvvvvv

1.Download and install the Windows version of espeak: http://espeak.sourceforge.net/download.html

2. set PATH=%PATH%;"C:\Program Files (x86)\eSpeak\command_line"_

3. Install .msi from https://github.com/espeak-ng/espeak-ng/releases

4.Enter environment variable

    1.PHONEMIZER_ESPEAK_LIBRARY="c:\Program Files\eSpeak NG\libespeak-ng.dll"
    2.PHONEMIZER_ESPEAK_PATH =“c:\Program Files\eSpeak NG”

and Restart your Computer.
