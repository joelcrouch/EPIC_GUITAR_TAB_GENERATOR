"""
Module for handling audio recording from microphone
"""
import os
import wave
import pyaudio
import time
import numpy as np
from datetime import datetime

class AudioRecorder:
    def __init__(self, output_dir="data"):
        """Initialize the audio recorder with default settings"""
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk = 1024
        self.output_dir = output_dir
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.filename = None
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def start_recording(self, max_seconds=None):
        """Start recording audio from the microphone"""
        self.frames = []
        self.is_recording = True
        
        # Generate a filename based on current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(self.output_dir, f"recording_{timestamp}.wav")
        
        # Open the stream
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        print(f"Recording started. Saving to {self.filename}")
        
        # Record for a maximum amount of time if specified
        if max_seconds:
            start_time = time.time()
            while self.is_recording and time.time() - start_time < max_seconds:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
            self.stop_recording()
        else:
            # If no time limit, recording will continue until stop_recording is called
            pass
    
    def record_frame(self):
        """Record a single frame of audio data"""
        if self.is_recording and self.stream:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
                return True
            except Exception as e:
                print(f"Error recording frame: {e}")
                return False
        return False
    
    def stop_recording(self):
        """Stop recording and save the audio to a WAV file"""
        if self.is_recording and self.stream:
            self.is_recording = False
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
            # Save the recorded audio to a WAV file
            self._save_wav()
            print(f"Recording stopped. Saved to {self.filename}")
            return self.filename
        return None
    
    def _save_wav(self):
        """Save recorded frames to a WAV file"""
        if len(self.frames) > 0:
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
    
    def get_audio_data(self):
        """Convert the recorded frames to a numpy array for analysis"""
        if not self.frames:
            return None
        
        # Convert byte data to numpy array
        data = np.frombuffer(b''.join(self.frames), dtype=np.int16)
        return data
    
    def close(self):
        """Clean up and release resources"""
        if self.stream:
            self.stream.close()
        self.audio.terminate()
        
    def __del__(self):
        """Destructor to ensure resources are released"""
        self.close()