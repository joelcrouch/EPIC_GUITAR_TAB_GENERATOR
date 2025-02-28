# Guitar Tab Generator App

A Python-based desktop application for recording guitar audio, detecting the pitch, and generating guitar tablature. This app provides an easy way to transcribe played notes into guitar tab format and display them to users.

## Features

- **Audio Recording**: Records guitar audio using the microphone and saves it as a `.wav` file.
- **Pitch Detection**: Analyzes the recorded audio to detect the frequencies of the played notes.
- **Guitar Note Mapping**: Maps detected frequencies to corresponding guitar notes (e.g., E, A, D, etc.).
- **Tab Generation**: Converts the detected notes into a guitar tab format.
- **UI**: Provides a basic interface to interact with the app and control the recording process.

## Tech Stack

- **Python**: Main language for development.
- **PyAudio**: For recording audio through the microphone.
- **Librosa** or **Aubio**: For pitch detection from the audio file.
- **tkinter** (or another Python GUI library): For the user interface.
- **pytest**: For unit testing the application functionality.
- **wave**: To save audio recordings as `.wav` files.

## Requirements

Before running the app, you'll need to set up your environment and install the required libraries.

### 1. Set up a virtual environment

Create a virtual environment for the project to keep dependencies isolated:

```bash
python3 -m venv env
```
Activate the environment:

On Windows:
```bash
.\env\Scripts\activate
```
On macOS/Linux:
```bash
    source env/bin/activate
```


2. Install the required dependencies

Run the following command to install the required libraries from requirements.txt:
```bash
pip install -r requirements.txt
```

If you don't have the requirements.txt file yet, you can create one by running:
```bash
pip freeze > requirements.txt
```
This will list the libraries you’ve installed into a requirements.txt file.

3. Additional setup for PyAudio

If you encounter issues with PyAudio (especially on Linux), ensure you have the necessary dependencies installed:

    On Ubuntu:
```bash
    sudo apt-get install portaudio19-dev
    sudo apt-get install python3-pyaudio
```
TODO:  Running the Application  


Once the environment is set up and dependencies are installed, you can start the application.

    A. Record audio: Press the "Record" button to capture audio from your guitar.
    
    B. Analyze pitch: Once the recording is done, the app will detect the frequencies of the notes.
    
    C. Generate guitar tab: The detected frequencies are then mapped to corresponding guitar notes and displayed in tablature format.

Testing

Unit tests are included to validate the core functionality of the app. You can run the tests using pytest.
Running tests:
```bash
pytest -s
```
I suggest using -s flag just to see what is happening with output.  It instills more trust if i can see the steps as the app steps through its functionality.  A little bit of 'insert print statement' debugging, but confidence is higher.

Example tests:

    Audio recording creates a .wav file.
    Recording is a valid .wav file (with proper number of channels, sample width, and framerate).

Folder Structure

Here's how the project files are organized:


```bash
guitar-tab-generator/
│── env/                      # Virtual environment (not included in Git)
│── src/                      # Main source code
│   │── __init__.py           # Marks this as a package
│   │── record_audio.py       # Handles audio recording
│   │── analyze_audio.py      # Uses Librosa/Aubio to detect notes
│   │── generate_tab.py       # Maps detected notes to tablature
│   │── ui.py                 # (Optional) GUI using Tkinter/PyQt
│── tests/                    # Unit and integration tests
│   │── __init__.py
│   │── test_audio_recording.py  # Tests for recording functionality
│   │── test_analyze_audio.py    # Tests for note detection
│   │── test_generate_tab.py     # Tests for tab generation
│── data/                     # Stores recorded audio files
│   │── samples/              # Sample recordings for testing
│── output/                   # Stores generated tablatures
│── requirements.txt          # Project dependencies
│── .gitignore                # Ignore unnecessary files (like env/)
│── README.md                 # Project description and setup instructions
│── main.py                   # Entry point (runs the app)


```



Contributing

Feel free to fork the repository, create issues, and submit pull requests. Contributions are welcome!