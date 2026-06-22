# xmusic - Scale Tool

**xmusic** is a Django-based web application designed for musicians. It renders an interactive fretboard diagram that displays scales and chords across different keys, instruments, and tunings.

## Features

- **Modes**: Choose between exploring **Scales** or **Chords**.
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
- **Instruments and Tunings**: 
  - **Guitar**: Standard, Drop D, Half-Step Down, D Standard, Drop C, DADGAD, Open G, Open D
  - **Bass (4-String)**: Standard, Drop D, Drop C
  - **Bass (5-String)**: Standard
- **Display Modes**: View the fretboard information in three different formats:
  - Degrees (Scale steps)
  - Notes (Actual musical notes, e.g., A#, C)
  - Intervals

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
