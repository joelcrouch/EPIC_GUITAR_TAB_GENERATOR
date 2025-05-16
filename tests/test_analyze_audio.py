"""
Tests for the audio analysis functionality
"""
import os
import pytest
import numpy as np
from src.analyze_audio import AudioAnalyzer

class TestAudioAnalyzer:
    def setup_method(self):
        """Set up test environment"""
        self.analyzer = AudioAnalyzer()
    
    def test_initialization(self):
        """Test that the analyzer initializes with correct settings"""
        assert self.analyzer.min_freq > 0
        assert self.analyzer.max_freq > self.analyzer.min_freq
        assert isinstance(self.analyzer.note_frequencies, dict)
        assert len(self.analyzer.note_frequencies) > 0
    
    def test_note_frequency_generation(self):
        """Test that note frequencies are generated correctly"""
        # Standard guitar open strings should be in the frequency dictionary
        guitar_strings = {
            'E2': 82.41,
            'A2': 110.00,
            'D3': 146.83,
            'G3': 196.00,
            'B3': 246.94,
            'E4': 329.63
        }
        
        for note, expected_freq in guitar_strings.items():
            # Find the closest note in our generated frequencies
            closest_note = None
            min_diff = float('inf')
            
            for gen_note, gen_freq in self.analyzer.note_frequencies.items():
                if gen_note.startswith(note[0]) and gen_note.endswith(note[1:]):
                    diff = abs(gen_freq - expected_freq)
                    if diff < min_diff:
                        min_diff = diff
                        closest_note = gen_note
            
            # Check that we found the note and it's close to the expected frequency
            assert closest_note is not None
            assert min_diff < 1.0  # Should be within 1 Hz of the expected frequency
    
    def test_map_to_guitar_note(self):
        """Test mapping frequencies to guitar notes and positions"""
        # Test with open string frequencies
        test_cases = [
            (82.41, 'E2', 6, 0),  # Low E string
            (110.00, 'A2', 5, 0),  # A string
            (146.83, 'D3', 4, 0),  # D string
            (196.00, 'G3', 3, 0),  # G string
            (246.94, 'B3', 2, 0),  # B string
            (329.63, 'E4', 1, 0)   # High E string
        ]
        
        for freq, expected_note, expected_string, expected_fret in test_cases:
            note, string, fret = self.analyzer._map_to_guitar_note(freq)
            
            # Note might have slight differences in naming (e.g., E2 vs E2)
            assert note[0] == expected_note[0]  # Same note letter
            assert note[-1] == expected_note[-1]  # Same octave
            assert string == expected_string
            assert fret == expected_fret
    
    def test_frequency_outside_range(self):
        """Test handling frequencies outside the guitar range"""
        # Test with frequency below guitar range
        note, string, fret = self.analyzer._map_to_guitar_note(20.0)  # Below E2
        
        # Should still map to a note, but not to a guitar position
        assert note is not None
        assert string is None or fret is None
        
        # Test with frequency above guitar range
        note, string, fret = self.analyzer._map_to_guitar_note(2000.0)  # Above E6
        
        # Should still map to a note, but might not map to a valid guitar position
        assert note is not None