# Guitar Tab Generator

A Python-based desktop application for recording guitar audio, detecting the pitch, and generating guitar tablature. This app provides an easy way to transcribe played notes into guitar tab format and display them to users.

## Features

- **Audio Recording**: Records guitar audio using the microphone and saves it as a `.wav` file.
- **Pitch Detection**: Analyzes the recorded audio to detect the frequencies of the played notes.
- **Guitar Note Mapping**: Maps detected frequencies to corresponding guitar notes (e.g., E, A, D, etc.).
- **Tab Generation**: Converts the detected notes into a guitar tab format.
- **UI**: Provides a clean tkinter interface to interact with the app and control the recording process.

## Screenshots

(add these when its running)

## Tech Stack

- **Python 3.10**: Main language for development
- **PyAudio**: For recording audio through the microphone
- **Librosa**: For pitch detection from the audio file using pYIN algorithm
- **tkinter**: For the user interface (included with Python)
- **pytest**: For unit testing the application functionality
- **wave**: To save audio recordings as `.wav` files (Python standard library)

## Requirements

### Prerequisites

- **Anaconda or Miniconda** installed on your system
- A microphone or audio interface connected to your computer

## Installation & Setup

### Method 1: Using environment.yml (Recommended)

This is the easiest and most reliable method:

```bash
# 1. Clone or navigate to the project directory
cd guitar-tab-generator

# 2. Create the conda environment from the file
conda env create -f environment.yml

# 3. Activate the environment
conda activate guitar-tab

# 4. Verify installation
python -c "import pyaudio, librosa; print('All dependencies installed!')"
```

### Method 2: Manual conda installation

If you prefer to create the environment manually:

```bash
# 1. Create a new conda environment with Python 3.10
conda create -n guitar-tab python=3.10

# 2. Activate the environment
conda activate guitar-tab

# 3. Install dependencies from conda-forge
conda install -c conda-forge pyaudio librosa pytest numpy scipy soundfile numba

# 4. Verify installation
python -c "import pyaudio, librosa; print('All dependencies installed!')"
```

### Platform-Specific Notes

#### macOS
```bash
# If you have issues with PyAudio on macOS, you may need:
brew install portaudio
conda install -c conda-forge pyaudio
```

#### Linux (Ubuntu/Debian)
```bash
# Install portaudio system library
sudo apt-get update
sudo apt-get install portaudio19-dev

# Then install conda packages
conda install -c conda-forge pyaudio librosa pytest
```

#### Windows
```bash
# Conda usually handles everything automatically on Windows
# If you have issues, try:
conda install -c conda-forge pyaudio
```

## Using the App

### Starting the Application

```bash
# Make sure your conda environment is activated
conda activate guitar-tab

# Run the application
python main.py
```

### Recording and Generating Tabs

1. **Record**
   - Connect your guitar to your computer via an audio interface or use a microphone positioned near your guitar
   - Click the "🎙️ Record" button to start recording
   - Play some notes or a melody on your guitar (single notes work best)
   - Click "⏹️ Stop" when you're done
   - You'll see the recording duration and file path in the output

2. **Generate Tablature**
   - Click the "🔍 Analyze" button to process the recording
   - The application will detect the notes and display them in tab format
   - Both standard tab and detailed note information will be shown

3. **Save the Tab**
   - Click the "💾 Save Tab" button to save the generated tab as a text file
   - Choose your desired location and filename
   - The tab file can be opened in any text editor

4. **Clear Output**
   - Click "🗑️ Clear" to clear the output area and start fresh

### How It Works

1. The application records audio through your computer's microphone using **PyAudio**
2. The recorded audio is saved as a `.wav` file in the `data/` directory
3. **Librosa** (a Python library for audio analysis) uses the pYIN algorithm to detect pitches in the recording
4. The detected frequencies are mapped to the closest guitar notes
5. The notes are intelligently positioned on the appropriate strings and frets to create readable guitar tablature
6. The resulting tab is displayed in the application and can be saved for future reference

## Testing

Unit tests are included to validate the core functionality of the app. You can run the tests using pytest.

### Running Tests

```bash
# Make sure your conda environment is activated
conda activate guitar-tab

# Run all tests with verbose output
pytest -s tests/

# Run specific test file
pytest -s tests/test_audio_recording.py

# Run with more details
pytest -v -s tests/
```

The `-s` flag shows print statements during tests, which helps you see what's happening step-by-step. This builds confidence that everything is working correctly!

### Example Tests

- Audio recording creates a `.wav` file
- Recording is a valid `.wav` file (with proper number of channels, sample width, and framerate)
- Multiple recordings can be made sequentially
- Recording duration is calculated correctly

## Folder Structure

```
guitar-tab-generator/
├── src/                          # Main source code
│   ├── __init__.py               # Package initialization
│   ├── record_audio.py           # Handles audio recording
│   ├── analyze_audio.py          # Pitch detection and note mapping
│   ├── generate_tab.py           # Tablature generation
│   └── ui.py                     # GUI using tkinter
├── tests/                        # Unit and integration tests
│   ├── __init__.py
│   ├── test_audio_recording.py  # Tests for recording functionality
│   ├── test_analyze_audio.py    # Tests for note detection (TODO)
│   └── test_generate_tab.py     # Tests for tab generation (TODO)
├── data/                         # Stores recorded audio files
│   └── samples/                  # Sample recordings for testing
├── output/                       # Stores generated tablatures
├── environment.yml               # Conda environment specification
├── requirements.txt              # Dependency list (for reference)
├── .gitignore                    # Ignore unnecessary files
├── README.md                     # This file
└── main.py                       # Entry point (runs the app)
```

## Managing Your Environment

```bash
# Activate environment
conda activate guitar-tab

# Deactivate environment
conda deactivate

# Update all packages
conda update --all

# List all packages in environment
conda list

# Remove environment (if needed)
conda env remove -n guitar-tab

# Export environment to share with others
conda env export > environment.yml
```

## Limitations and Known Issues

- The pitch detection works best with **clean, single-note** guitar playing
- Fast or complex passages may not be accurately transcribed
- Background noise can affect the quality of note detection
- Currently only supports **standard guitar tuning** (E A D G B E)
- Chords and multiple simultaneous notes are not well detected

## Future Enhancements

- [ ] Support for different guitar tunings
- [ ] Improved detection of chords and multiple notes played simultaneously
- [ ] Rhythm detection to include timing information in the tab
- [ ] Visual representation of the detected notes on a guitar fretboard
- [ ] Export to Guitar Pro or other tab formats
- [ ] Real-time pitch detection (no recording needed)
- [ ] Adjustable confidence thresholds in UI
- [ ] Support for bass guitar (4-string and 5-string)

## Troubleshooting

### "No module named 'pyaudio'" or similar import errors
```bash
# Make sure your conda environment is activated
conda activate guitar-tab

# Reinstall the problematic package
conda install -c conda-forge pyaudio
```

### "No audio input device found"
- Make sure your microphone/audio interface is connected
- Check your system audio settings
- Try running a test: `python -c "import pyaudio; p=pyaudio.PyAudio(); print(p.get_device_count())"`

### Poor note detection
- Record in a quiet environment
- Play single notes clearly with good separation
- Make sure your guitar is in tune
- Try playing louder or moving closer to the microphone
- Use an audio interface instead of built-in microphone for better quality

### Tests failing
```bash
# Make sure all dependencies are up to date
conda update --all

# Try reinstalling the environment
conda env remove -n guitar-tab
conda env create -f environment.yml
```

## Contributing

Feel free to fork the repository, create issues, and submit pull requests. Contributions are welcome!

Some areas that need work:
- Additional test coverage (analyze_audio.py, generate_tab.py)
- Chord detection algorithms
- Real-time processing
- Better UI/UX improvements

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Librosa** team for the excellent audio analysis library
- **PyAudio** for making audio I/O accessible in Python
- All contributors and testers