"""
Audio recording module for the Guitar Tab Generator.
Handles microphone input and saves recordings as WAV files.
"""
import pyaudio
import wave
import os
from datetime import datetime

class AudioRecorder:
    def __init__(self, 
                 sample_rate=44100,
                 channels=1, 
                 chunk_size=4096,
                 audio_format=pyaudio.paInt16):
        """
        Initialize the audio recorder with specified parameters.
        
        Args:
            sample_rate: Sampling rate in Hz (default: 44100)
            channels: Number of audio channels (default: 1 for mono)
            chunk_size: Size of audio chunks to read (default: 1024)
            audio_format: PyAudio format (default: 16-bit int)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_format = audio_format
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
    def start_recording(self):
        """Start recording audio from the microphone."""
        if self.is_recording:
            print("Already recording!")
            return
            
        print("Starting recording...")
        self.frames = []
        self.is_recording = True
        
        self.stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
    def record_chunk(self):
        """Record a single chunk of audio data."""
        if not self.is_recording:
            return
            
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
        self.frames.append(data)
        
    def stop_recording(self):
        """Stop recording and close the audio stream."""
        if not self.is_recording:
            print("Not currently recording!")
            return
            
        print("Stopping recording...")
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
    def save_recording(self, filename=None, output_dir="data"):
        """
        Save the recorded audio to a WAV file.
        
        Args:
            filename: Output filename (generates timestamp-based name if None)
            output_dir: Directory to save the file (default: "data")
            
        Returns:
            Path to the saved file
        """
        if not self.frames:
            print("No audio data to save!")
            return None
            
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
        filepath = os.path.join(output_dir, filename)
        
        # Write the WAV file
        print(f"Saving recording to {filepath}...")
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            
        print(f"Recording saved successfully!")
        return filepath
        
    def cleanup(self):
        """Clean up PyAudio resources."""
        if self.stream:
            self.stream.close()
        self.audio.terminate()
        
    def get_recording_duration(self):
        """Calculate the duration of the current recording in seconds."""
        if not self.frames:
            return 0.0
        total_frames = len(self.frames) * self.chunk_size
        return total_frames / self.sample_rate