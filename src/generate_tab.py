"""
Tablature generation module for the Guitar Tab Generator.
Converts detected notes into readable guitar tablature.
"""
import os

class TabGenerator:
    def __init__(self, time_resolution=0.25):
        """
        Initialize the tab generator.
        
        Args:
            time_resolution: Time spacing between columns in seconds (default: 0.25)
        """
        self.time_resolution = time_resolution
        
    def group_notes_by_time(self, notes):
        """
        Group notes into time slots based on time resolution.
        
        Args:
            notes: List of note dictionaries from AudioAnalyzer
            
        Returns:
            Dictionary mapping time slots to lists of notes
        """
        time_slots = {}
        
        for note in notes:
            # Round time to nearest time slot
            slot = round(note['time'] / self.time_resolution) * self.time_resolution
            
            if slot not in time_slots:
                time_slots[slot] = []
            time_slots[slot].append(note)
            
        return time_slots
        
    def merge_duplicate_notes(self, notes_in_slot):
        """
        Merge duplicate notes on the same string within a time slot.
        Keeps the note with highest confidence.
        
        Args:
            notes_in_slot: List of notes in the same time slot
            
        Returns:
            List of unique notes (one per string)
        """
        string_notes = {}
        
        for note in notes_in_slot:
            string = note['string']
            if string is None:
                continue
                
            # Keep note with highest confidence for each string
            if string not in string_notes or note['confidence'] > string_notes[string]['confidence']:
                string_notes[string] = note
                
        return list(string_notes.values())
        
    def generate_tab(self, notes, max_width=80):
        """
        Generate guitar tablature from detected notes.
        
        Args:
            notes: List of note dictionaries
            max_width: Maximum width of tab before line break
            
        Returns:
            String containing formatted tablature
        """
        if not notes:
            return "No notes detected.\n"
            
        # Group notes by time
        time_slots = self.group_notes_by_time(notes)
        sorted_times = sorted(time_slots.keys())
        
        # Initialize tab lines for 6 strings
        strings = {
            1: 'e|',  # High E
            2: 'B|',
            3: 'G|',
            4: 'D|',
            5: 'A|',
            6: 'E|'   # Low E
        }
        
        tab_lines = []
        current_lines = {i: strings[i] for i in range(1, 7)}
        
        print(f"Generating tab for {len(sorted_times)} time slots...")
        
        for time in sorted_times:
            slot_notes = time_slots[time]
            merged_notes = self.merge_duplicate_notes(slot_notes)
            
            # Find max fret width for alignment
            max_fret_width = 1
            for note in merged_notes:
                if note['fret'] is not None:
                    max_fret_width = max(max_fret_width, len(str(note['fret'])))
                    
            # Add notes to strings
            for string_num in range(1, 7):
                # Find note for this string
                note_for_string = None
                for note in merged_notes:
                    if note['string'] == string_num:
                        note_for_string = note
                        break
                        
                if note_for_string and note_for_string['fret'] is not None:
                    fret_str = str(note_for_string['fret'])
                    # Pad fret number
                    current_lines[string_num] += fret_str + '-' * (max_fret_width - len(fret_str) + 1)
                else:
                    current_lines[string_num] += '-' * (max_fret_width + 1)
                    
            # Check if we need to start a new line
            if len(current_lines[1]) >= max_width:
                # Add current lines to tab
                for i in range(1, 7):
                    tab_lines.append(current_lines[i])
                tab_lines.append('')  # Empty line between sections
                
                # Reset lines
                current_lines = {i: strings[i] for i in range(1, 7)}
                
        # Add remaining lines
        if len(current_lines[1]) > 2:  # More than just "e|"
            for i in range(1, 7):
                tab_lines.append(current_lines[i])
                
        return '\n'.join(tab_lines)
        
    def generate_detailed_tab(self, notes):
        """
        Generate a detailed tablature with note names and timing information.
        
        Args:
            notes: List of note dictionaries
            
        Returns:
            String containing detailed tablature
        """
        if not notes:
            return "No notes detected.\n"
            
        output = []
        output.append("=" * 70)
        output.append("DETAILED GUITAR TABLATURE")
        output.append("=" * 70)
        output.append("")
        
        for i, note in enumerate(notes, 1):
            time_str = f"{note['time']:.2f}s"
            note_str = f"{note['note']}{note['octave']}" if note['note'] else "Unknown"
            freq_str = f"{note['frequency']:.2f} Hz" if note['frequency'] else "N/A"
            string_str = f"String {note['string']}" if note['string'] else "Unknown"
            fret_str = f"Fret {note['fret']}" if note['fret'] is not None else "N/A"
            conf_str = f"{note['confidence']*100:.1f}%"
            
            output.append(f"Note {i:3d}: {time_str:>8} | {note_str:>4} | {freq_str:>10} | "
                         f"{string_str:>8} | {fret_str:>7} | Conf: {conf_str}")
                         
        output.append("")
        output.append("=" * 70)
        return '\n'.join(output)
        
    def save_tab(self, tab_content, filename=None, output_dir="output"):
        """
        Save tablature to a text file.
        
        Args:
            tab_content: Tab content as string
            filename: Output filename (generates default if None)
            output_dir: Directory to save the file
            
        Returns:
            Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tab_{timestamp}.txt"
            
        filepath = os.path.join(output_dir, filename)
        
        print(f"Saving tab to {filepath}...")
        with open(filepath, 'w') as f:
            f.write(tab_content)
            
        print("Tab saved successfully!")
        return filepath