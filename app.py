import assemblyai as aai
from flask import Flask, render_template, jsonify
import threading

app = Flask(__name__)
aai.settings.api_key = "59993d1eba9a4a459f946ccd654d3014"

transcriber = None
transcribed_text = ""

def on_open():
    print("Transcription started!")

def on_data(transcript: aai.RealtimeTranscript):
    global transcribed_text
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        transcribed_text += transcript.text + "\n"
        print("Transcribed:", transcript.text)  # Verify text here
    else:
        print("Received partial:", transcript.text)


def on_error(error):
    print("Error:", error)

def on_close():
    print("Transcription stopped!")

def start_transcription():
    global transcriber
    microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
    transcriber = aai.RealtimeTranscriber(
        encoding=aai.AudioEncoding.pcm_mulaw,
        sample_rate=16_000,
        word_boost=["aws", "azure", "google cloud"],
        end_utterance_silence_threshold=500,
        on_open=on_open,
        on_data=on_data,
        on_error=on_error,
        on_close=on_close,
    )

    for audio_data in microphone_stream:
        if transcriber is not None:
            transcriber.stream(audio_data)
        else:
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    global transcribed_text
    transcribed_text = ""  # Clear previous transcript
    threading.Thread(target=start_transcription).start()
    return jsonify({"message": "Transcription started!"})


@app.route('/stop')
def stop():
    global transcriber
    if transcriber is not None:
        transcriber.close()
        transcriber = None
        print("Transcriber closed")
    return jsonify({"message": "Transcription stopped!"})


# @app.route('/transcript')
# def transcript():
#     global transcribed_text
#     print("Transcript:", transcribed_text)
#     return jsonify({"transcript": transcribed_text or ""})
@app.route('/transcript')
def transcript():
    global transcribed_text
    return jsonify({"transcript": transcribed_text})


if __name__ == "__main__":
    app.run(debug=True)
