import os
import pytest
import sys
import wave
# Add the src folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from record_audio import record_audio

#TEST 1: does the recording make a file? DO we actually have input?

def test_audio_recording_creates_file():
    filename="test_recording.wav"  #put something in data?
    record_audio(filename, duration=2)  #record for 2 secnds adjust as needed
    assert os.path.exists(filename)
    assert os.path.getsize(filename)>0
    os.remove(filename)

#test2: is the recording a 'good' .wav file
def test_audio_reocording_is_valid_wav():
    filename="test_recording.wav"  #put something in data?
    record_audio(filename, duration=2) 

    with wave.open(filename, 'rb') as wav_file:
        assert wav_file.getnchannels()==1
        assert wav_file.getsampwidth()>0
        assert wav_file.getframerate()>0  

    os.remove(filename)


#think aobout putting these into a for loop and having some setup function get
# the filename and cleanup, then just call the for loop, or add a for loop to each 
#test and test more->or a combination?
