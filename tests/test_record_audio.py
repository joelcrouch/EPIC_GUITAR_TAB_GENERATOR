"""
Unit tests for audio recording functionality.
"""
import pytest
import os
import wave
import time
from src.record_audio import AudioRecorder


class TestAudioRecorder:
    """Test cases for the AudioRecorder class."""
    
    @pytest.fixture
    def recorder(self):
        """Create a recorder instance for testing."""
        print("\n[TEST SETUP] Creating AudioRecorder instance...")
        rec = AudioRecorder()
        yield rec
        print("[TEST CLEANUP] Cleaning up AudioRecorder...")
        rec.cleanup()
        
    def test_recorder_initialization(self, recorder):
        """Test that the recorder initializes with correct parameters."""
        print("[TEST] Testing recorder initialization...")
        assert recorder.sample_rate == 44100
        assert recorder.channels == 1
        assert recorder.chunk_size == 4096
        assert recorder.is_recording == False
        assert len(recorder.frames) == 0
        print("[PASS] Recorder initialized correctly")
        
    def test_start_recording(self, recorder):
        """Test that recording can be started."""
        print("[TEST] Testing start_recording...")
        recorder.start_recording()
        assert recorder.is_recording == True
        assert recorder.stream is not None
        print("[PASS] Recording started successfully")
        recorder.stop_recording()
        
    def test_stop_recording(self, recorder):
        """Test that recording can be stopped."""
        print("[TEST] Testing stop_recording...")
        recorder.start_recording()
        time.sleep(0.1)  # Record for a brief moment
        recorder.stop_recording()
        assert recorder.is_recording == False
        assert recorder.stream is None
        print("[PASS] Recording stopped successfully")
        
    def test_record_and_save(self, recorder, tmp_path):
        """Test recording audio and saving to a file."""
        print("[TEST] Testing record_and_save...")
        
        # Start recording
        print("  Starting recording for 1 second...")
        recorder.start_recording()
        
        # Record for 1 second
        start_time = time.time()
        while time.time() - start_time < 1.0:
            recorder.record_chunk()
            time.sleep(0.01)
            
        # Stop recording
        print("  Stopping recording...")
        recorder.stop_recording()
        
        # Save to temp directory
        output_file = os.path.join(tmp_path, "test_recording.wav")
        print(f"  Saving to {output_file}...")
        saved_path = recorder.save_recording(
            filename="test_recording.wav",
            output_dir=str(tmp_path)
        )
        
        # Verify file exists
        assert os.path.exists(saved_path)
        print(f"  File created: {saved_path}")
        
        # Verify it's a valid WAV file
        print("  Verifying WAV file format...")
        with wave.open(saved_path, 'rb') as wf:
            assert wf.getnchannels() == recorder.channels
            assert wf.getsampwidth() == recorder.audio.get_sample_size(recorder.audio_format)
            assert wf.getframerate() == recorder.sample_rate
            num_frames = wf.getnframes()
            print(f"  WAV file properties:")
            print(f"    - Channels: {wf.getnchannels()}")
            print(f"    - Sample width: {wf.getsampwidth()} bytes")
            print(f"    - Frame rate: {wf.getframerate()} Hz")
            print(f"    - Number of frames: {num_frames}")
            
        # Verify duration is approximately 1 second
        duration = recorder.get_recording_duration()
        print(f"  Recording duration: {duration:.2f} seconds")
        assert 0.9 <= duration <= 1.5  # Allow some tolerance
        
        print("[PASS] Recording and saving successful")
        
    def test_get_recording_duration(self, recorder):
        """Test that recording duration is calculated correctly."""
        print("[TEST] Testing get_recording_duration...")
        
        # Initially should be 0
        assert recorder.get_recording_duration() == 0.0
        print("  Initial duration: 0.0s")
        
        # Record for a short time
        recorder.start_recording()
        start_time = time.time()
        while time.time() - start_time < 0.5:
            recorder.record_chunk()
            time.sleep(0.01)
        recorder.stop_recording()
        
        # Check duration
        duration = recorder.get_recording_duration()
        print(f"  Recorded duration: {duration:.2f}s")
        assert 0.4 <= duration <= 0.6  # Should be around 0.5 seconds
        
        print("[PASS] Duration calculation correct")
        
    def test_multiple_recordings(self, recorder, tmp_path):
        """Test that multiple recordings can be made sequentially."""
        print("[TEST] Testing multiple recordings...")
        
        for i in range(3):
            print(f"  Recording #{i+1}...")
            recorder.start_recording()
            
            # Record briefly
            for _ in range(20):
                recorder.record_chunk()
                time.sleep(0.01)
                
            recorder.stop_recording()
            
            # Save
            filename = f"recording_{i}.wav"
            saved_path = recorder.save_recording(
                filename=filename,
                output_dir=str(tmp_path)
            )
            
            assert os.path.exists(saved_path)
            print(f"    Saved: {saved_path}")
            
        print("[PASS] Multiple recordings successful")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])