import pyaudio 
import wave

def record_audio(filename="output.wav", duration=5, sample_rate=44100, chunk_size=1024):
    """
    Records audio from the user's microphone and saves it as a .wav file.
    
    :param filename: The name of the output .wav file.
    :param duration: Recording duration in seconds.
    :param sample_rate: The sample rate of the recording.
    :param chunk_size: The buffer size of each recorded chunk.
    """
    audio=pyaudio.PyAudio()
    stream= audio.open(format=pyaudio.paInt16, 
                       channels=1, 
                       rate=sample_rate,
                       input=True,
                       frames_per_buffer=chunk_size)
    
    print("Recording...")#likely wont go into ui but might be a placeholder for
    #ui stuff

    frames=[]
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data=stream.read(chunk_size)
        frames.append(data)

    print("Recording done.")
     
     #cleanup
    stream.start_stream()
    stream.close()
    audio.terminate()

    #now save it!
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))