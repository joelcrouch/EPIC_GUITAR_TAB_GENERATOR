"""
Audio analysis module for the Guitar Tab Generator.
Detects pitches from recorded audio and maps them to guitar notes.
"""
import librosa
import numpy as np

class AudioAnalyzer:
    # Standard guitar tuning (from lowest to highest string)
    STANDARD_TUNING = {
        'E2': 82.41,   # Low E string (6th string)
        'A2': 110.00,  # A string (5th string)
        'D3': 146.83,  # D string (4th string)
        'G3': 196.00,  # G string (3rd string)
        'B3': 246.94,  # B string (2nd string)
        'E4': 329.63   # High E string (1st string)
    }
    
    # Note names
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def __init__(self, hop_length=512, frame_length=2048):
        """
        Initialize the audio analyzer.
        
        Args:
            hop_length: Number of samples between successive frames
            frame_length: Length of the windowed signal for FFT
        """
        self.hop_length = hop_length
        self.frame_length = frame_length
        
    def load_audio(self, filepath):
        """
        Load an audio file.
        
        Args:
            filepath: Path to the audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        print(f"Loading audio file: {filepath}")
        y, sr = librosa.load(filepath, sr=None)
        print(f"Audio loaded: {len(y)} samples at {sr} Hz ({len(y)/sr:.2f} seconds)")
        return y, sr
        
    def detect_pitches(self, audio_data, sample_rate, fmin=80, fmax=1000):
        """
        Detect pitches in the audio data using librosa's pyin algorithm.
        
        Args:
            audio_data: Audio time series
            sample_rate: Sampling rate
            fmin: Minimum frequency to detect (Hz)
            fmax: Maximum frequency to detect (Hz)
            
        Returns:
            Tuple of (frequencies, times, confidences)
        """
        print("Detecting pitches...")
        
        # Use pyin for pitch detection (probabilistic YIN)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio_data,
            fmin=fmin,
            fmax=fmax,
            sr=sample_rate,
            hop_length=self.hop_length,
            frame_length=self.frame_length
        )
        
        # Calculate time for each frame
        times = librosa.frames_to_time(
            np.arange(len(f0)),
            sr=sample_rate,
            hop_length=self.hop_length
        )
        
        print(f"Detected {len(f0)} pitch frames")
        return f0, times, voiced_probs
        
    def frequency_to_note(self, frequency):
        """
        Convert a frequency to the nearest note name and octave.
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            Tuple of (note_name, octave, cents_off)
        """
        if frequency is None or np.isnan(frequency) or frequency <= 0:
            return None, None, None
            
        # A4 = 440 Hz is our reference
        a4_freq = 440.0
        a4_midi = 69
        
        # Calculate MIDI note number
        midi_note = 12 * np.log2(frequency / a4_freq) + a4_midi
        midi_note_rounded = int(round(midi_note))
        
        # Calculate cents off from the nearest note
        cents_off = 100 * (midi_note - midi_note_rounded)
        
        # Get note name and octave
        note_index = midi_note_rounded % 12
        octave = (midi_note_rounded // 12) - 1
        note_name = self.NOTE_NAMES[note_index]
        
        return note_name, octave, cents_off
        
    def find_string_and_fret(self, frequency):
        """
        Find the best guitar string and fret for a given frequency.
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            Tuple of (string_number, fret_number, string_name)
            String numbers: 1=high E, 6=low E
        """
        if frequency is None or np.isnan(frequency) or frequency <= 0:
            return None, None, None
            
        # Calculate MIDI note number
        a4_freq = 440.0
        a4_midi = 69
        target_midi = 12 * np.log2(frequency / a4_freq) + a4_midi
        
        # Define string tunings with MIDI numbers
        strings = [
            (6, 'E2', 40),  # Low E
            (5, 'A2', 45),  # A
            (4, 'D3', 50),  # D
            (3, 'G3', 55),  # G
            (2, 'B3', 59),  # B
            (1, 'E4', 64),  # High E
        ]
        
        best_match = None
        min_fret = 100
        
        # Try each string
        for string_num, string_name, open_string_midi in strings:
            fret = round(target_midi - open_string_midi)
            
            # Only consider valid fret positions (0-24)
            if 0 <= fret <= 24:
                # Prefer lower frets and higher strings
                if fret < min_fret or (fret == min_fret and best_match and string_num < best_match[0]):
                    min_fret = fret
                    best_match = (string_num, fret, string_name)
                    
        return best_match if best_match else (None, None, None)
        
    def analyze_recording(self, filepath, confidence_threshold=0.5):
        """
        Analyze a recording and extract guitar notes with timing.
        
        Args:
            filepath: Path to the audio file
            confidence_threshold: Minimum confidence for including a note
            
        Returns:
            List of detected notes with (time, frequency, note, octave, string, fret)
        """
        # Load audio
        audio_data, sample_rate = self.load_audio(filepath)
        
        # Detect pitches
        frequencies, times, confidences = self.detect_pitches(audio_data, sample_rate)
        
        # Process detected pitches
        notes = []
        for i, (freq, time, conf) in enumerate(zip(frequencies, times, confidences)):
            if conf >= confidence_threshold and not np.isnan(freq):
                note_name, octave, cents = self.frequency_to_note(freq)
                string_num, fret, string_name = self.find_string_and_fret(freq)
                
                notes.append({
                    'time': time,
                    'frequency': freq,
                    'note': note_name,
                    'octave': octave,
                    'cents_off': cents,
                    'string': string_num,
                    'fret': fret,
                    'string_name': string_name,
                    'confidence': conf
                })
                
        print(f"Extracted {len(notes)} notes from recording")
        return notes