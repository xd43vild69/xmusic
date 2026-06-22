# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the development server
python manage.py runserver

# Run tests
python manage.py test

# Run a single test
python manage.py test main.tests.TestCaseName

# Apply migrations
python manage.py migrate
```

The project uses a `.venv` virtualenv — activate it with `source .venv/bin/activate` before running commands.

## Architecture

**xmusic** is a Django web app that renders a fretboard diagram showing which frets to play for a given musical scale, key, and instrument.

### Request flow

1. User submits the form on `home.html` (scale, key, instrument) → `POST /button_action/`
2. `views.py` maps the selection to a scale interval pattern (`get_scale`) and instantiates `Manager` with the chosen `Instrument` enum
3. `Manager` builds per-string note sequences (`set_strings_tool`) and marks which notes belong to the scale (`set_scale`)
4. `set_matrix` in `views.py` converts the string data into a 2D grid (strings × frets) of `Note` objects
5. The matrix is passed to the template and rendered as a fretboard table

### Key modules

- `main/manager/manager.py` — core music logic: builds chromatic note sequences per string, walks the scale interval pattern to mark scale tones and root notes
- `main/instrument.py` — `Instrument` enum (Guitar=6 strings, Bass4=4, Bass5=5); also encodes standard tuning per instrument inside `Manager.__init__`
- `main/entities/note.py` — `Note` data class; `step` (1-based scale degree, 0 = not in scale), `root` flag, `name` (e.g. `"A#"`)
- `main/entities/node.py` — `Node` (older/unused; `Note` is the active entity)
- `main/views.py` — Django views + `get_scale` which maps scale name strings to interval patterns (`'H'`=half step, `'W'`=whole, `'WH'`=augmented)
- `xmusic/templates/home.html` — single-page template; renders the fretboard matrix

### Scale interval encoding

Scales are lists of interval tokens: `'H'` (1 semitone), `'W'` (2 semitones), `'WH'` (3 semitones). `Manager.get_steps` converts these. The list length determines how many notes are in the scale; `set_scale` iterates until `interval == len(scale)`.
