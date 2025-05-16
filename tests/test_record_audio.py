"""
Tests for the audio recording functionality
"""
import os
import pytest
import wave
import numpy as np
from src.record_audio import AudioRecorder

class TestAudioRecorder:
    def setup_method(self):
        # Create a temporary directory for test recordings
        self.test_dir = "test_data"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
        # Initialize recorder with test directory
        self.recorder = AudioRecorder(output_dir=self.test_dir)
    
    def teardown_method(self):
        # Clean up test files
        for file in os.listdir(self.test_dir):
            if file.startswith("recording_") and file.endswith(".wav"):
                try:
                    os.remove(os.path.join(self.test_dir, file))
                except:
                    pass
        
        # Close the recorder
        self.recorder.close()
    
    def test_initialization(self):
        """Test that the recorder initializes with correct settings"""
        assert self.recorder.channels == 1
        assert self.recorder.sample_rate == 44100
        assert self.recorder.format is not None
        assert os.path.exists(self.test_dir)
    
    def test_save_wav_empty(self):
        """Test that _save_wav handles empty frames"""
        self.recorder.frames = []
        self.recorder.filename = os.path.join(self.test_dir, "empty_test.wav")
        # This should not create a file since frames is empty
        self.recorder._save_wav()
        assert not os.path.exists(self.recorder.filename)
    
    def test_mock_recording(self):
        """
        Test recording functionality by creating mock frames and saving them
        
        This doesn't actually record audio but tests the file saving mechanism
        """
        # Create some mock audio data (1 second of silence)
        mock_audio = np.zeros(44100, dtype=np.int16)
        mock_frames = [mock_audio.tobytes()]
        
        # Set up the recorder with mock data
        self.recorder.frames = mock_frames
        self.recorder.filename = os.path.join(self.test_dir, "mock_recording.wav")
        
        # Save the mock recording
        self.recorder._save_wav()
        
        # Check that the file was created
        assert os.path.exists(self.recorder.filename)
        
        # Validate the WAV file
        with wave.open(self.recorder.filename, 'rb') as wf:
            assert wf.getnchannels() == self.recorder.channels
            assert wf.getframerate() == self.recorder.sample_rate
            assert wf.getsampwidth() == 2  # 16-bit audio = 2 bytes per sample
    
    def test_get_audio_data(self):
        """Test converting frames to numpy array"""
        # Create some mock audio data
        mock_audio = np.array([1000, 2000, 3000], dtype=np.int16)
        self.recorder.frames = [mock_audio.tobytes()]
        
        # Get the audio data as numpy array
        audio_data = self.recorder.get_audio_data()
        
        # Check the conversion
        assert isinstance(audio_data, np.ndarray)
        assert audio_data.dtype == np.int16
        assert len(audio_data) == 3
        assert np.array_equal(audio_data, mock_audio)
    
    def test_get_audio_data_empty(self):
        """Test getting audio data when no frames are available"""
        self.recorder.frames = []
        audio_data = self.recorder.get_audio_data()
        assert audio_data is None
#think aobout putting these into a for loop and having some setup function get
# the filename and cleanup, then just call the for loop, or add a for loop to each 
#test and test more->or a combination?
