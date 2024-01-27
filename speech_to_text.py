#pip install pvcheetah pyaudio struct keyboard

import pvcheetah
import pyaudio
import struct
import keyboard

# Create an instance of the speech-to-text object with your AccessKey
handle = pvcheetah.create(access_key="L4ZEhdjTxAEZx6X+w3f2LCzpUrsoJXDsEw/NecUKqj4tuRNVp1e1IA==")

# Initialize PyAudio and open a stream
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=handle.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=handle.frame_length)

# Transcribe audio stream in real-time
transcribed_text = ""

while True:
    # Check if ESC key is pressed
    if keyboard.is_pressed('esc'):
        break

    # Get the next audio frame from the stream
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)

    # Process the audio frame and get the partial transcript
    partial_transcript, is_endpoint = handle.process(pcm)

    # Accumulate the transcribed text
    transcribed_text += partial_transcript
    # if transcribed text has more than 100 characters, reset it
    if len(transcribed_text) > 100:
        transcribed_text = ""
    print(transcribed_text)

    # If the audio frame is an endpoint, print the accumulated transcript
    if is_endpoint:
        print(transcribed_text)
        transcribed_text = ""

# Cleanup resources
audio_stream.stop_stream()
audio_stream.close()
pa.terminate()

