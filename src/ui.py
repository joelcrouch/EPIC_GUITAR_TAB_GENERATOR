"""
User interface module for the Guitar Tab Generator.
Provides a tkinter-based GUI for recording and analyzing guitar audio.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import os

from src.record_audio import AudioRecorder
from src.analyze_audio import AudioAnalyzer
from src.generate_tab import TabGenerator


class GuitarTabApp:
    def __init__(self, root):
        """Initialize the Guitar Tab Generator application."""
        self.root = root
        self.root.title("Guitar Tab Generator")
        self.root.geometry("800x600")
        
        # Initialize components
        self.recorder = AudioRecorder()
        self.analyzer = AudioAnalyzer()
        self.tab_generator = TabGenerator()
        
        # State variables
        self.recording_thread = None
        self.is_recording = False
        self.current_recording_file = None
        self.current_notes = None
        
        # Create UI
        self.create_widgets()
        
        # Bind cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        """Create and layout all UI widgets."""
        # Title
        title_label = tk.Label(
            self.root,
            text="🎸 Guitar Tab Generator",
            font=("Arial", 20, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Control Frame
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Recording controls
        self.record_button = ttk.Button(
            control_frame,
            text="🎙️ Record",
            command=self.toggle_recording,
            width=15
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = ttk.Button(
            control_frame,
            text="🔍 Analyze",
            command=self.analyze_recording,
            state=tk.DISABLED,
            width=15
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(
            control_frame,
            text="💾 Save Tab",
            command=self.save_tab,
            state=tk.DISABLED,
            width=15
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(
            control_frame,
            text="🗑️ Clear",
            command=self.clear_output,
            width=15
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to record",
            font=("Arial", 10),
            fg="green",
            pady=5
        )
        self.status_label.pack()
        
        # Recording time label
        self.time_label = tk.Label(
            self.root,
            text="Duration: 0.0s",
            font=("Arial", 9),
            fg="gray"
        )
        self.time_label.pack()
        
        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Output area
        output_label = tk.Label(
            self.root,
            text="Output",
            font=("Arial", 12, "bold")
        )
        output_label.pack(anchor=tk.W, padx=10)
        
        # Scrolled text for output
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.NONE,
            font=("Courier", 9),
            height=20
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Add horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(self.output_text, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.output_text.config(xscrollcommand=h_scrollbar.set)
        h_scrollbar.config(command=self.output_text.xview)
        
    def toggle_recording(self):
        """Start or stop audio recording."""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start recording audio in a separate thread."""
        self.is_recording = True
        self.recorder.start_recording()
        
        # Update UI
        self.record_button.config(text="⏹️ Stop")
        self.status_label.config(text="Recording... Play your guitar!", fg="red")
        self.analyze_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self.record_loop, daemon=True)
        self.recording_thread.start()
        
        # Start time update
        self.update_recording_time()
        
    def record_loop(self):
        """Continuously record audio chunks while recording is active."""
        while self.is_recording:
            self.recorder.record_chunk()
            time.sleep(0.01)  # Small delay to prevent CPU hogging
            
    def update_recording_time(self):
        """Update the recording time display."""
        if self.is_recording:
            duration = self.recorder.get_recording_duration()
            self.time_label.config(text=f"Duration: {duration:.1f}s")
            self.root.after(100, self.update_recording_time)
            
    def stop_recording(self):
        """Stop recording and save the audio file."""
        self.is_recording = False
        self.recorder.stop_recording()
        
        # Update UI
        self.record_button.config(text="🎙️ Record")
        self.status_label.config(text="Recording stopped. Click Analyze to generate tab.", fg="blue")
        
        # Save the recording
        self.current_recording_file = self.recorder.save_recording()
        
        if self.current_recording_file:
            duration = self.recorder.get_recording_duration()
            self.append_output(f"Recording saved: {self.current_recording_file}\n")
            self.append_output(f"Duration: {duration:.2f} seconds\n\n")
            self.analyze_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Error saving recording", fg="red")
            
    def analyze_recording(self):
        """Analyze the recorded audio and generate tablature."""
        if not self.current_recording_file or not os.path.exists(self.current_recording_file):
            messagebox.showerror("Error", "No recording found to analyze!")
            return
            
        # Update UI
        self.status_label.config(text="Analyzing audio... Please wait.", fg="orange")
        self.analyze_button.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # Analyze in a separate thread to keep UI responsive
            analysis_thread = threading.Thread(target=self._do_analysis, daemon=True)
            analysis_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.status_label.config(text="Analysis failed", fg="red")
            self.analyze_button.config(state=tk.NORMAL)
            
    def _do_analysis(self):
        """Perform the actual analysis (runs in separate thread)."""
        try:
            self.append_output("Starting analysis...\n")
            
            # Analyze recording
            self.current_notes = self.analyzer.analyze_recording(self.current_recording_file)
            
            if not self.current_notes:
                self.root.after(0, lambda: self.status_label.config(
                    text="No notes detected. Try recording again with clearer audio.",
                    fg="orange"
                ))
                self.append_output("\nNo notes detected. Tips:\n")
                self.append_output("- Play single notes clearly\n")
                self.append_output("- Reduce background noise\n")
                self.append_output("- Play louder or closer to microphone\n\n")
                return
                
            # Generate tab
            tab = self.tab_generator.generate_tab(self.current_notes)
            detailed_tab = self.tab_generator.generate_detailed_tab(self.current_notes)
            
            # Display results
            self.append_output("\n" + "="*70 + "\n")
            self.append_output("GUITAR TABLATURE\n")
            self.append_output("="*70 + "\n\n")
            self.append_output(tab)
            self.append_output("\n\n")
            self.append_output(detailed_tab)
            self.append_output("\n")
            
            # Update UI
            self.root.after(0, lambda: self.status_label.config(
                text=f"Analysis complete! Found {len(self.current_notes)} notes.",
                fg="green"
            ))
            self.root.after(0, lambda: self.save_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))
            
        except Exception as e:
            self.append_output(f"\nError during analysis: {str(e)}\n")
            self.root.after(0, lambda: self.status_label.config(
                text="Analysis failed",
                fg="red"
            ))
            self.root.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))
            
    def save_tab(self):
        """Save the generated tablature to a file."""
        if not self.current_notes:
            messagebox.showerror("Error", "No tab to save! Analyze a recording first.")
            return
            
        # Ask user for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="output"
        )
        
        if filename:
            try:
                # Get tab content
                tab = self.tab_generator.generate_tab(self.current_notes)
                detailed_tab = self.tab_generator.generate_detailed_tab(self.current_notes)
                
                full_content = f"{tab}\n\n{detailed_tab}"
                
                # Save to file
                with open(filename, 'w') as f:
                    f.write(full_content)
                    
                messagebox.showinfo("Success", f"Tab saved to:\n{filename}")
                self.status_label.config(text="Tab saved successfully!", fg="green")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save tab: {str(e)}")
                
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.delete(1.0, tk.END)
        self.status_label.config(text="Output cleared", fg="gray")
        
    def append_output(self, text):
        """Append text to the output area."""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.root.update()
        
    def on_closing(self):
        """Clean up resources when closing the application."""
        if self.is_recording:
            self.stop_recording()
        self.recorder.cleanup()
        self.root.destroy()


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = GuitarTabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()