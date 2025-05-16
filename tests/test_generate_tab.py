"""
Tests for the tab generation functionality
"""
import os
import pytest
from src.generate_tab import TabGenerator

class TestTabGenerator:
    def setup_method(self):
        """Set up test environment"""
        self.tab_generator = TabGenerator()
        self.test_output_dir = "test_output"
        if not os.path.exists(self.test_output_dir):
            os.makedirs(self.test_output_dir)
    
    def teardown_method(self):
        """Clean up test files"""
        for file in os.listdir(self.test_output_dir):
            if file.endswith(".txt"):
                try:
                    os.remove(os.path.join(self.test_output_dir, file))
                except:
                    pass
    
    def test_initialization(self):
        """Test that the tab generator initializes with correct settings"""
        assert len(self.tab_generator.guitar_strings) == 6
        assert len(self.tab_generator.empty_tab) == 6
        for line in self.tab_generator.empty_tab:
            assert line.startswith('-')
    
    def test_empty_tab_generation(self):
        """Test generating an empty tab"""
        tab = self.tab_generator.generate_tab([])
        assert len(tab.split('\n')) == 6  # 6 strings
        for line in tab.split('\n'):
            assert line.startswith(('E|', 'A|', 'D|', 'G|', 'B|'))
            assert line.endswith('|')
    
    def test_generate_tab_with_notes(self):
        """Test generating a tab with some notes"""
        # Sample detected notes: (time, note, string, fret)
        notes = [
            (0.0, 'E2', 6, 0),   # Low E string open
            (0.5, 'A2', 5, 0),   # A string open
            (1.0, 'D3', 4, 0),   # D string open
            (1.5, 'G3', 3, 0),   # G string open
            (2.0, 'B3', 2, 0),   # B string open
            (2.5, 'E4', 1, 0)    # High E string open
        ]
        
        tab = self.tab_generator.generate_tab(notes)
        
        # Check that the tab contains all strings
        assert len(tab.split('\n')) == 6
        
        # Check that each note appears in the correct position
        lines = tab.split('\n')
        assert '0' in lines[0]  # High E string (index 0)
        assert '0' in lines[1]  # B string
        assert '0' in lines[2]  # G string
        assert '0' in lines[3]  # D string
        assert '0' in lines[4]  # A string
        assert '0' in lines[5]  # Low E string
    
    def test_generate_tab_with_fretted_notes(self):
        """Test generating a tab with fretted notes"""
        # Sample detected notes with various frets
        notes = [
            (0.0, 'F2', 6, 1),    # Low E string, 1st fret
            (0.5, 'C3', 5, 3),    # A string, 3rd fret
            (1.0, 'F3', 4, 3),    # D string, 3rd fret
            (1.5, 'C4', 3, 5),    # G string, 5th fret
            (2.0, 'E4', 2, 5),    # B string, 5th fret
            (2.5, 'A4', 1, 5)     # High E string, 5th fret
        ]
        
        tab = self.tab_generator.generate_tab(notes)
        
        # Check that the tab contains all strings
        assert len(tab.split('\n')) == 6
        
        # Check that each fret number appears in the correct position
        lines = tab.split('\n')
        assert '5' in lines[0]  # High E string, 5th fret
        assert '5' in lines[1]  # B string, 5th fret
        assert '5' in lines[2]  # G string, 5th fret
        assert '3' in lines[3]  # D string, 3rd fret
        assert '3' in lines[4]  # A string, 3rd fret
        assert '1' in lines[5]  # Low E string, 1st fret
    
    def test_save_tab_to_file(self):
        """Test saving a tab to a file"""
        # Generate a simple tab
        tab = self.tab_generator.generate_tab([])
        
        # Save it to a file
        output_path = os.path.join(self.test_output_dir, "test_tab.txt")
        result = self.tab_generator.save_tab_to_file(tab, output_path)
        
        # Check that the file was created
        assert result is True
        assert os.path.exists(output_path)
        
        # Check the file contents
        with open(output_path, 'r') as f:
            content = f.read()
            assert content == tab
    
    def test_format_tab(self):
        """Test formatting tab lines with string labels"""
        # Create some mock tab lines
        tab_lines = ['-1--', '-2--', '-3--', '-4--', '-5--', '-6--']
        
        # Format the tab
        formatted_tab = self.tab_generator._format_tab(tab_lines)
        
        # Check the formatting
        expected_lines = [
            'E|-1--|',
            'B|-2--|',
            'G|-3--|',
            'D|-4--|',
            'A|-5--|',
            'E|-6--|'
        ]
        assert formatted_tab == '\n'.join(expected_lines)