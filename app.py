import assemblyai as aai
import openai
import elevenlabs
from queue import Queue
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.aai_api_key
openai.api_key = os.openai_api_key
elevenlabs.api_key = os.elevenlabs_api_key

transcript_queue = Queue()

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    if isinstance(transcript, aai.RealtimeFinalTranscript):
        transcript_queue.put(transcript.text + '')
        print("User:", transcript.test, end="\r\n")
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occurred: ", error)

def handle_conversation():
    while True:
        transcriber = aai.RealtimeTranscriber(
            on_data=on_data,
            on_error=on_error,
            sample_rate=44_100,
        )

        transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream()
        transcriber.stream(microphone_stream)
        transcriber.close()
        transcript_result = transcript_queue.get()
    
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5',
            messages = [
                {"role": "system", "content": "You are a highly skilled AI, answer the questions given within a maximum of 1000 characters."},
                {"role": "system", "content": transcript_result}
            ]
        )

        text = response['choices'][0]['messages']['content']

        audio = elevenlabs.generate(
            text=text,
            voice="Adam"
        )

        print("\nAI:", text, end="\r\n")

        elevenlabs.play(audio)

def main():
    handle_conversation()
    return 0

if __name__ == "__main__":
    main()