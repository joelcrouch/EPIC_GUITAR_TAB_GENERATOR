Epic: Guitar Tab Generator App
1. Recording Audio from the User

    User Story: As a user, I want to record audio of my guitar playing, so that I can have my performance transcribed into guitar tablature.

Acceptance Criteria:

    A button labeled "Record" allows the user to start and stop recording.
    The app records audio and saves it as a .wav file.
    The user is notified when the recording is complete.

Sub-tasks:

    Set up a basic UI with a "Record" button (using Tkinter or PyQt).
    Implement audio recording using PyAudio or sounddevice.
    Save the audio as a .wav file.

Estimated Time: 2-3 days
2. Pitch Detection from Audio

    User Story: As a user, I want the app to detect the pitch of the notes in the audio I recorded, so that I can have my performance analyzed.

Acceptance Criteria:

    The app extracts the pitch (frequency) from the .wav file.
    The detected pitch is displayed in the UI for the user to review.

Sub-tasks:

    Integrate Librosa or Aubio for pitch detection.
    Write a function to extract the fundamental frequency from the recorded audio.
    Display the detected pitch on the UI or log it for testing.

Estimated Time: 2-3 days
3. Mapping Frequency to Guitar Notes

    User Story: As a user, I want the app to map the detected pitch to a specific guitar note and fret position, so that I can see where to play the note on the guitar.

Acceptance Criteria:

    The app maps the detected pitch to the closest guitar note (e.g., E, A, D, G, B, e).
    The app displays the corresponding fret position for the note.

Sub-tasks:

    Implement the mapping logic from frequency to guitar notes (e.g., dictionary of guitar string frequencies, formula for calculating frets).
    Verify the pitch-to-note mapping with sample recordings.
    Display the note and fret position in the UI.

Estimated Time: 2-3 days
4. Generating Guitar Tab

    User Story: As a user, I want the app to generate guitar tablature from the detected notes, so that I can view a readable transcription of my performance.

Acceptance Criteria:

    The app generates a guitar tab string from the detected notes and their fret positions.
    The tab is displayed in a human-readable format (e.g., string-by-string layout).

Sub-tasks:

    Implement a function to convert note and fret positions into guitar tab format.
    Display the generated tab in the app's UI.
    Ensure the format adheres to the standard guitar tab format.

Estimated Time: 2-3 days
5. Saving the Tab to a Database

    User Story: As a user, I want the app to save the generated tablature to a database, so that I can retrieve and review it later.

Acceptance Criteria:

    The app stores the generated guitar tab in a database (e.g., SQLite).
    The app associates the tablature with a track name or unique identifier.

Sub-tasks:

    Set up a simple database (e.g., SQLite) with a table for storing tabs.
    Implement a function to save the generated tab and track name into the database.
    Implement functionality to retrieve and display saved tabs from the database.

Estimated Time: 2-3 days
6. Basic User Interface (UI) for Displaying Tabs

    User Story: As a user, I want a simple interface to view my recorded audio, detected pitch, and generated guitar tab, so that I can review and download my work.

Acceptance Criteria:

    The app should display the recorded audio status, detected pitch, and generated tab on the UI.
    The UI should have a button to play back the recording and a button to download the tab.
    The UI should be simple and user-friendly.

Sub-tasks:

    Set up a basic UI with Tkinter or PyQt.
    Display the recorded audio file, pitch detection results, and generated tab.
    Implement buttons to allow the user to replay the recording and download the tab.

Estimated Time: 2-3 days
7. Testing and Debugging

    User Story: As a developer, I want to ensure that all components (recording, pitch detection, tab generation, database) work together correctly so that the app functions as expected.

Acceptance Criteria:

    Perform unit testing for each module (recording, pitch detection, tab generation, database).
    Perform end-to-end testing with the full workflow (record → detect pitch → map to note → generate tab → save to database).
    Ensure that any bugs are fixed and edge cases are handled (e.g., very short or long recordings, extreme pitch variations).

Sub-tasks:

    Write unit tests for pitch detection and tab generation functions.
    Test the full pipeline with sample audio files.
    Debug and fix any issues.

Estimated Time: 3-4 days
Putting it All Together: Sprint 1 Plan

Assuming a 2-week sprint (10 working days), this could be your Sprint 1 Plan:

Week 1:

    Day 1-2: Set up UI and basic recording functionality (Recording audio using PyAudio or sounddevice).
    Day 3-4: Implement pitch detection using Librosa or Aubio.
    Day 5-6: Map detected frequencies to guitar notes and display them.

Week 2: 4. Day 7-8: Implement tab generation logic and display in the UI. 5. Day 9: Set up database and save generated tab. 6. Day 10: Testing and debugging, including unit tests and full workflow testing.(kinda done in situ, but i i will leave this here for now, b/c i might get lazy and do them last)

Basic testing:
Summary of Tests:

    Recording Audio: Ensures that the app can record and save audio correctly.
    Pitch Detection: Verifies that the app detects the correct pitch.
    Frequency-to-Note Mapping: Checks that the detected frequency maps to the correct guitar note and fret.
    Tab Generation: Confirms that the app generates guitar tabs correctly from the detected notes.
    Database Storage: Tests if the tab is saved to and retrievable from the database.
    UI Updates: Ensures that the UI correctly displays the generated tab.

This will be our project structure, loosely
epic-guitar-tab-generator/
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



So attempting to do this project as a tdd project.  Let us see how it works, and will we have fewer bugs.  Also, this is the protottype.  If this goes well i will polish it up, and submit it to the app stores. 


HOW TO: 
So first I am going to write some unit tests for the first user story, but before I do that, I need to create a virtual environment:

```
bash
python3 -m venv epic 
source env/bin/activate
```

For the first task, we need to add some info to our requirements.txt  
Make it from cl:
```
bash

touch requirements.txt
```
Open it up and add 'pytest(unit testing), pyaudio(for recording audio), wave (for saving .wav files).  

Ok. fast forward.  I made the virtual env, (.env) activated it and ran pip install -r requirements.txt, and got this error: 

```
bash 
  (some other output that worked)...
  Building wheel for pyaudio (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Building wheel for pyaudio (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [15 lines of output]
      running bdist_wheel
      running build
      running build_py
      creating build/lib.linux-x86_64-cpython-312/pyaudio
      copying src/pyaudio/__init__.py -> build/lib.linux-x86_64-cpython-312/pyaudio
      running build_ext
      building 'pyaudio._portaudio' extension
      creating build/temp.linux-x86_64-cpython-312/src/pyaudio
      x86_64-linux-gnu-gcc -fno-strict-overflow -Wsign-compare -DNDEBUG -g -O2 -Wall -fPIC -I/usr/local/include -I/usr/include -I/home/joel/epic/env/include -I/usr/include/python3.12 -c src/pyaudio/device_api.c -o build/temp.linux-x86_64-cpython-312/src/pyaudio/device_api.o
      In file included from src/pyaudio/device_api.c:1:
      src/pyaudio/device_api.h:7:10: fatal error: Python.h: No such file or directory
          7 | #include "Python.h"
            |          ^~~~~~~~~~
      compilation terminated.
      error: command '/usr/bin/x86_64-linux-gnu-gcc' failed with exit code 1
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pyaudio
Failed to build pyaudio
ERROR: Could not build wheels for pyaudio, which is required to install pyproject.toml-based projects

```

So after bashing around with pyaudio documentation, i think we need some dependencies:

```
bash
sudo apt-get update
sudo apt-get install python3-dev portaudio19-dev libsndfile1
Dont do this:  It is in req.txt. pip install pyaudio (reinstall!!, maybe optional, who knows)

```

Err. You are installing these system wide. Dont forget to deactivate and reactivate the .env.

OK. Now when you run source env\bin\activate and python3 install -r requirements.txt, it should work.  (FYI: I am working on Ubuntu 24.04, you can adapt these commands to windows, arch, centos, bsd, whatever you want.)
Check it with this : 

```
bash

python3 -c "import pyaudio; print(pyaudio.__version__)"

```

Finally, lets write some code!
OH wait. go ahead and investigate the docs here: https://pypi.org/project/PyAudio/  and here: https://docs.python.org/3/library/wave.html   They are pretty straightforward and you can almost use boilerplate code from them and just adapt it for your needs. Great.

