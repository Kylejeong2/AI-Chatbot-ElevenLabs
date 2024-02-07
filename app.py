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

    