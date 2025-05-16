"""
User interface for the Guitar Tab Generator application
"""
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import time

from src.record_audio import AudioRecorder
from src.analyze_audio import AudioAnalyzer
from src.generate_tab import TabGenerator

class TabGeneratorApp:
    def __init__(self, root):
        """Initialize the application UI"""
        self.root = root
        self.recorder = AudioRecorder(output_dir="data")
        self.analyzer = AudioAnalyzer()
        self.tab_generator = TabGenerator()
        
        # Create output directories if they don't exist
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("output"):
            os.makedirs("output")
        
        # Recording state
        self.is_recording = False
        self.record_thread = None
        self.current_audio_file = None
        
        # Create UI elements
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and layout all UI widgets"""
        # Main frame with padding
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Guitar Tab Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Control frame (buttons)
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Recording controls
        self.record_button = tk.Button(control_frame, text="Record", command=self._toggle_recording, bg="#ff7f7f")
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        self.analyze_button = tk.Button(control_frame, text="Analyze", command=self._analyze_audio, state=tk.DISABLED)
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Load file button
        self.load_button = tk.Button(control_frame, text="Load Audio File", command=self._load_audio_file)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Save tab button
        self.save_button = tk.Button(control_frame, text="Save Tab", command=self._save_tab, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(fill=tk.X, pady=(5, 0))
        
        # Tab display area
        tab_frame = tk.LabelFrame(main_frame, text="Guitar Tab")
        tab_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.tab_text = scrolledtext.ScrolledText(tab_frame, wrap=tk.NONE, font=("Courier", 12))
        self.tab_text.pack(fill=tk.BOTH, expand=True)
        
        # Set default tab display
        default_tab = self.tab_generator._format_tab(self.tab_generator.empty_tab)
        self.tab_text.insert(tk.END, default_tab)
        self.tab_text.config(state=tk.DISABLED)
        
        # Notes display area
        notes_frame = tk.LabelFrame(main_frame, text="Detected Notes")
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=5, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        self.notes_text.config(state=tk.DISABLED)
    
    def _toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.record_button.config(text="Stop", bg="#7fff7f")
            self.load_button.config(state=tk.DISABLED)
            self.analyze_button.config(state=tk.DISABLED)
            self.status_var.set("Recording...")
            
            # Clear previous results
            self.tab_text.config(state=tk.NORMAL)
            self.tab_text.delete(1.0, tk.END)
            self.tab_text.insert(tk.END, self.tab_generator._format_tab(self.tab_generator.empty_tab))
            self.tab_text.config(state=tk.DISABLED)
            
            self.notes_text.config(state=tk.NORMAL)
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.config(state=tk.DISABLED)
            
            # Start recording in a separate thread
            self.record_thread = threading.Thread(target=self._record_audio)
            self.record_thread.daemon = True
            self.record_thread.start()
        else:
            # Stop recording
            self.is_recording = False
            self.recorder.stop_recording()
            self.record_button.config(text="Record", bg="#ff7f7f")
            self.analyze_button.config(state=tk.NORMAL)
            self.load_button.config(state=tk.NORMAL)
            self.status_var.set("Recording stopped. Ready to analyze.")
    
    def _record_audio(self):
        """Record audio in a separate thread"""
        self.recorder.start_recording()
        while self.is_recording:
            self.recorder.record_frame()
            time.sleep(0.01)  # Small delay to prevent high CPU usage
        
        # When recording is stopped
        self.current_audio_file = self.recorder.filename
    
    def _analyze_audio(self):
        """Analyze the recorded audio and generate tab"""
        if not self.current_audio_file:
            messagebox.showwarning("Warning", "No audio file to analyze.")
            return
        
        self.status_var.set(f"Analyzing audio file: {os.path.basename(self.current_audio_file)}...")
        self.root.update()
        
        try:
            # Analyze audio
            detected_notes = self.analyzer.analyze_audio_file(self.current_audio_file)
            
            # Display detected notes
            self.notes_text.config(state=tk.NORMAL)
            self.notes_text.delete(1.0, tk.END)
            if detected_notes:
                for time, note, string, fret in detected_notes:
                    position_info = f"String {string}, Fret {fret}" if string and fret else "Unknown position"
                    self.notes_text.insert(tk.END, f"Time: {time:.2f}s, Note: {note}, {position_info}\n")
            else:
                self.notes_text.insert(tk.END, "No notes detected. Try recording again with clearer audio.")
            self.notes_text.config(state=tk.DISABLED)
            
            # Generate and display tab
            tab_text = self.tab_generator.generate_tab(detected_notes)
            self.tab_text.config(state=tk.NORMAL)
            self.tab_text.delete(1.0, tk.END)
            self.tab_text.insert(tk.END, tab_text)
            self.tab_text.config(state=tk.DISABLED)
            
            # Enable save button
            self.save_button.config(state=tk.NORMAL)
            
            self.status_var.set("Analysis complete. Tab generated.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")
            self.status_var.set("Analysis failed.")
    
    def _load_audio_file(self):
        """Load an existing audio file for analysis"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=(("WAV files", "*.wav"), ("All files", "*.*"))
        )
        
        if file_path:
            self.current_audio_file = file_path
            self.status_var.set(f"Audio file loaded: {os.path.basename(file_path)}")
            self.analyze_button.config(state=tk.NORMAL)
    
    def _save_tab(self):
        """Save the generated tab to a text file"""
        if self.tab_text.get(1.0, tk.END).strip() == "":
            messagebox.showwarning("Warning", "No tab to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Tab As",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
            initialdir="output"
        )
        
        if file_path:
            tab_text = self.tab_text.get(1.0, tk.END)
            try:
                with open(file_path, 'w') as file:
                    file.write(tab_text)
                self.status_var.set(f"Tab saved to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save tab: {str(e)}")