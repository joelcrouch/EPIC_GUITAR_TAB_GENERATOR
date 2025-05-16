"""
Module for generating guitar tablature from detected notes
"""

class TabGenerator:
    def __init__(self):
        """Initialize the tab generator with default settings"""
        # Standard guitar tuning (from low to high)
        self.guitar_strings = ['E', 'A', 'D', 'G', 'B', 'E']
        
        # Empty tab representation (6 strings)
        self.empty_tab = ['-' * 60 for _ in range(6)]
        
    def generate_tab(self, detected_notes):
        """
        Generate guitar tab from a list of detected notes
        
        Args:
            detected_notes: List of (time, note, string_num, fret) tuples
        
        Returns:
            String representation of the guitar tab
        """
        if not detected_notes:
            return self._format_tab(self.empty_tab)
            
        # Initialize an empty tab with enough space
        max_time = max([time for time, _, _, _ in detected_notes]) if detected_notes else 0
        tab_length = int(max_time * 10) + 10  # Scale time to tab positions (10 chars per second)
        tab = ['-' * tab_length for _ in range(6)]
        
        # Place the notes in the tab
        for time, note, string_num, fret in detected_notes:
            if string_num is None or fret is None:
                continue
                
            # Convert time to position in the tab (10 chars per second)
            position = int(time * 10)
            
            # Make sure we don't exceed tab length
            if position >= tab_length - 2:
                continue
                
            # Insert the fret number at the correct position
            string_idx = string_num - 1  # 0-indexed
            
            # Handle double-digit fret numbers
            fret_str = str(fret)
            if len(fret_str) == 1:
                # Single-digit fret
                tab[string_idx] = tab[string_idx][:position] + fret_str + tab[string_idx][position+1:]
            else:
                # Double-digit fret (ensure there's enough space)
                if position < tab_length - len(fret_str):
                    tab[string_idx] = tab[string_idx][:position] + fret_str + tab[string_idx][position+len(fret_str):]
        
        return self._format_tab(tab)
    
    def _format_tab(self, tab_lines):
        """Format the tab lines with string labels"""
        # Add string labels
        formatted_tab = []
        for i, line in enumerate(tab_lines):
            formatted_tab.append(f"{self.guitar_strings[i]}|{line}|")
        
        return '\n'.join(formatted_tab)
    
    def save_tab_to_file(self, tab_text, output_path):
        """Save the generated tab to a text file"""
        try:
            with open(output_path, 'w') as f:
                f.write(tab_text)
            return True
        except Exception as e:
            print(f"Error saving tab to file: {e}")
            return False