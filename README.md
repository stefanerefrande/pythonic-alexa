# Pythonic Alexa

Virtual Assistant project that transcribes voice audios into text and generates a response from an AI.

This project works with two different APIs:
- AssemblyAI API to transcribe the voice audio into written text
- OpenAI API to receive the question, interpret it and generate the answer


## Playing 
- You must have an account for each API the project is consuming from. You can register at their oficial websites.
- Run the script from command prompt 
- First interaction will be a check on the audio input device (it will send a confirmation once the device is ready)
- Pyaudio enables the device mic to listen to voice data
- The question is made
- The data is storaged and encoded
- The data is converted into text
- The data is sent to the API responsible for processing the text
- The answer to the question returns on the console right below the question

Curious fact: it is possible to set a whisper-listening-mode to capture whispered questions (we may need it sometimes!)
