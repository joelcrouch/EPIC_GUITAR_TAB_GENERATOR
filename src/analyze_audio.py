"""
Module for analyzing audio and detecting guitar notes
"""
import numpy as np
import librosa
import os

class AudioAnalyzer:
    def __init__(self):
        """Initialize the audio analyzer with guitar-specific settings"""
        # Standard guitar tuning frequencies for open strings (E2, A2, D3, G3, B3, E4)
        self.guitar_open_strings = {
            'E2': 82.41,
            'A2': 110.00,
            'D3': 146.83,
            'G3': 196.00,
            'B3': 246.94,
            'E4': 329.63
        }
        
        # Define the frequency range for guitar notes (from E2 to E6)
        self.min_freq = 75  # Just below E2
        self.max_freq = 1400  # Above E6
        
        # Note frequencies for mapping (all notes across the fretboard)
        self.note_frequencies = self._generate_note_frequencies()
        
    def _generate_note_frequencies(self):
        """Generate a dictionary of note frequencies across the guitar range"""
        # Base frequencies for the chromatic scale starting at C0
        base_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        base_freq = 16.35  # C0
        
        notes_dict = {}
        
        # Generate frequencies for all notes in our range
        for octave in range(2, 7):  # From octave 2 to 6 (covers guitar range)
            for i, note in enumerate(base_notes):
                freq = base_freq * (2 ** (octave + i/12))
                if self.min_freq <= freq <= self.max_freq:
                    note_name = f"{note}{octave}"
                    notes_dict[note_name] = freq
                    
        return notes_dict
    
    def analyze_audio_file(self, file_path):
        """
        Analyze an audio file to detect pitches and convert to guitar notes
        
        Returns a list of (time, note, string, fret) tuples
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # Load the audio file with librosa
        y, sr = librosa.load(file_path, sr=None)
        
        # Use librosa's pitch tracking
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        
        # Extract the strongest pitches over time
        times = librosa.times_like(pitches)
        detected_notes = []
        
        # Process each frame
        for t, time in enumerate(times):
            # Only process frames every 0.1 seconds to avoid excessive notes
            if t % int(sr/1024/10) != 0:
                continue
                
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            
            # Only proceed if the pitch is strong enough and in our frequency range
            if pitch > 0 and self.min_freq <= pitch <= self.max_freq:
                # Map to the closest guitar note
                note, string, fret = self._map_to_guitar_note(pitch)
                if note:
                    detected_notes.append((time, note, string, fret))
        
        return detected_notes
    
    def analyze_audio_data(self, audio_data, sample_rate):
        """
        Analyze audio data directly from a numpy array
        
        Returns a list of (time, note, string, fret) tuples
        """
        # Use librosa's pitch tracking on the numpy array
        pitches, magnitudes = librosa.piptrack(y=audio_data.astype(float), sr=sample_rate)
        
        # Extract the strongest pitches over time
        times = librosa.times_like(pitches)
        detected_notes = []
        
        # Process each frame
        for t, time in enumerate(times):
            # Only process frames every 0.1 seconds to avoid excessive notes
            if t % int(sample_rate/1024/10) != 0:
                continue
                
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            
            # Only proceed if the pitch is strong enough and in our frequency range
            if pitch > 0 and self.min_freq <= pitch <= self.max_freq:
                # Map to the closest guitar note
                note, string, fret = self._map_to_guitar_note(pitch)
                if note:
                    detected_notes.append((time, note, string, fret))
        
        return detected_notes
    
    def _map_to_guitar_note(self, frequency):
        """
        Map a frequency to the closest guitar note, string, and fret
        
        Returns a tuple of (note_name, string_number, fret_number)
        """
        # Find the closest note by frequency
        closest_note = None
        min_distance = float('inf')
        
        for note, note_freq in self.note_frequencies.items():
            distance = abs(frequency - note_freq)
            if distance < min_distance:
                min_distance = distance
                closest_note = note
        
        if not closest_note:
            return None, None, None
        
        # Map the note to a guitar string and fret
        # We try to find the most ergonomic position on the fretboard
        
        # Standard guitar tuning
        strings = ['E4', 'B3', 'G3', 'D3', 'A2', 'E2']
        string_num = None
        fret_num = None
        
        # Find which string and fret produces this note
        note_name = closest_note[:-1]  # Remove octave number
        note_octave = int(closest_note[-1])
        
        for i, string in enumerate(strings):
            string_name = string[:-1]  # Remove octave number
            string_octave = int(string[-1])
            
            # Find the semitone difference between the string and note
            note_index = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].index(note_name)
            string_index = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'].index(string_name)
            
            octave_diff = note_octave - string_octave
            semitones = octave_diff * 12 + (note_index - string_index)
            
            # If the note can be played on this string (within 15 frets)
            if 0 <= semitones <= 15:
                string_num = i + 1  # 1-indexed string number
                fret_num = semitones
                break
        
        # If we couldn't find a suitable string and fret, just return the note
        if string_num is None:
            return closest_note, None, None
            
        return closest_note, string_num, fret_num