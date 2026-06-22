# xmusic - Scale Tool

**xmusic** is a Django-based web application designed for musicians. It renders an interactive fretboard diagram that displays scales and chords across different keys, instruments, and tunings.

## Features

- **Modes**: Choose between exploring **Scales**, **Chords**, or **Progressions**.
- **Keys**: Supports all natural musical keys (A, B, C, D, E, F, G).
- **Scales**: Explore a wide variety of scales, including:
  - Major, Minor
  - Blues Minor, Blues Major
  - Mixolydian, Locrian, Octatonic
  - Dark 3, Dark 4, Dark 5
- **Chords**: Visualize different chord types, including:
  - Major, Minor
  - Maj7, Min7, Dom7
  - m7b5, Diminished, Augmented
- **Progressions (Root Tracking)**: Visually trace harmonic sequences on the fretboard. Available progressions:
  - Pop-Punk (I-V-vi-IV)
  - Blues-Metal (I-IV-V)
  - Jazz (ii-V-I)
  - Doo-Wop-Retro (I-vi-IV-V)
  - Andalusian-Descenso (i-VII-VI-V)
  - Epic Minor (i-VI-III-VII)
- **Instruments and Tunings**: 
  - **Guitar**: Standard, Drop D, Half-Step Down, D Standard, Drop C, DADGAD, Open G, Open D
  - **Bass (4-String)**: Standard, Drop D, Drop C
  - **Bass (5-String)**: Standard
- **Display Modes**: View the fretboard information in three different formats:
  - Degrees (Scale steps)
  - Notes (Actual musical notes, e.g., A#, C)
  - Intervals
- **Interactive Audio & Playback**: 
  - Click on any fret/dot on the fretboard to play the exact pitch for that note in the selected tuning.
  - Synthesized audio playback using the Web Audio API with realistic ADSR envelopes.
- **Interval Codex**: 
  - Hover over specific intervals in the Codex to highlight matching positions on the fretboard.
  - Click an interval to hear the acoustic relation (plays the root note followed by the selected interval) and read a descriptive breakdown of its emotional and mathematical characteristics.
- **Dynamic Fretboard Alignment**: The visual fretboard completely adapts its row headers (string names) to precisely match the selected alternative tuning dynamically.

## Architecture Overview

The application is built using **Django** and Python. 
- **User Interface**: A single-page template (`home.html`) with a responsive design renders the fretboard matrix.
- **Core Logic**: The backend calculates the chromatic note sequences per string and walks the scale interval patterns to mark the correct scale tones or chord notes (`main/manager/manager.py` and `main/views.py`).

## Installation & Running Locally

Ensure you have Python installed. The project uses a virtual environment.

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Testing & Maintenance

- **Apply migrations**:
  ```bash
  python manage.py migrate
  ```

- **Run all tests**:
  ```bash
  python manage.py test
  ```

- **Run a single test**:
  ```bash
  python manage.py test main.tests.TestCaseName
  ```
