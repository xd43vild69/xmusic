from django.shortcuts import render, redirect
from django.http import HttpResponse
from .manager.manager import Manager
from .instrument import Instrument
from .entities.note import Note

# Create your views here.

strings = 5

# Human-readable labels for the dynamic "now showing" header
INSTRUMENT_LABELS = {
    "bass4": "Bass 4 (Standard)",
    "bass4_drop_d": "Bass 4 (Drop D)",
    "bass4_drop_c": "Bass 4 (Drop C)",
    "bass5": "Bass 5",
    "guitar": "Guitar (Standard)",
    "guitar_drop_d": "Guitar (Drop D)",
    "guitar_half_step_down": "Guitar (Half-Step Down)",
    "guitar_d_standard": "Guitar (D Standard)",
    "guitar_drop_c": "Guitar (Drop C)",
    "guitar_dadgad": "Guitar (DADGAD)",
    "guitar_open_g": "Guitar (Open G)",
    "guitar_open_d": "Guitar (Open D)",
}

SCALE_LABELS = {
    "mayor": "Mayor", "minor": "Minor", "blues_minor": "Blues Minor",
    "blues_major": "Blues Mayor", "mixolydian": "Mixolydian", "locrian": "Locrian",
    "octatonic": "Octatonic", "dark_3": "Dark 3", "dark_4": "Dark 4", "dark_5": "Dark 5",
}

CHORD_LABELS = {
    "major": "Major", "minor": "Minor", "maj7": "Maj7", "min7": "Min7",
    "dom7": "Dom7", "m7b5": "m7b5", "dim": "Dim", "aug": "Aug",
}

PROGRESSION_LABELS = {
    "pop-punk": "Pop-Punk (I-V-vi-IV)", "blues-metal": "Blues-Metal (I-IV-V)",
    "jazz_ii_v_i": "Jazz (ii-V-I)", "doo_wop-Retro": "Doo-Wop-Retro (I-vi-IV-V)",
    "andalusian-descenso": "Andalusian-Descenso (i-VII-VI-V)",
    "epic_minor": "Epic Minor (i-VI-III-VII)",
}


def build_now_showing(mode, key, scale, chord, progression, instrument):
    if mode == "chord":
        selection = CHORD_LABELS.get(chord, chord)
    elif mode == "progression":
        selection = PROGRESSION_LABELS.get(progression, progression)
    else:
        selection = SCALE_LABELS.get(scale, scale)
    instrument_label = INSTRUMENT_LABELS.get(instrument, instrument)
    return f"{key} · {selection}", instrument_label

def get_scale(selected_scale):
    scale = []
    if selected_scale == "mayor":
        scale = ['H', 'W', 'W', 'H', 'W', 'W', 'W', 'H']
    elif selected_scale == "minor":
        scale = ['W', 'W', 'H', 'W', 'W', 'H', 'W', 'W']
    elif selected_scale == "blues_minor":
        scale = ['X', 'WH', 'W', 'H', 'H', 'WH', 'W']
    elif selected_scale == "blues_major":
        scale = ['X', 'W', 'H', 'H', 'WH', 'W', 'WH']
    elif selected_scale == "mixolydian":
        scale = ['W', 'W', 'W', 'H', 'W', 'W', 'H', 'W']
    elif selected_scale == "locrian":
        scale = ['W', 'H', 'W', 'W', 'H', 'W', 'W', 'W']
    elif selected_scale == "octatonic":
        scale = ['W', 'H', 'W', 'H', 'W', 'H', 'W', 'H', 'W']
    elif selected_scale == "dark_3":
        scale = ['W', 'H', 'W', 'H', 'W', 'H', 'H', 'W', 'W']
    elif selected_scale == "dark_4":
        scale = ['H','H', 'W', 'W', 'H', 'W', 'H', 'W', 'H']
    elif selected_scale == "dark_5":
        scale = ['H', 'H', 'W', 'H', 'W', 'W', 'H', 'W', 'H']
    elif selected_scale == "dark_6":
        scale = ['W', 'H', 'W', 'H', 'W', 'W', 'W', 'W']
    elif selected_scale == "dark_7":
        scale = ['H', 'H', 'W', 'H', 'W', 'H', 'H', 'WH', 'H']                
    return scale

def get_chord(selected_chord):
    chord = []
    if selected_chord == "major":
        chord = ['X', '4', '3', '5']
    elif selected_chord == "minor":
        chord = ['X', '3', '4', '5']
    elif selected_chord == "maj7":
        chord = ['X', '4', '3', '4', '1']
    elif selected_chord == "min7":
        chord = ['X', '3', '4', '3', '2']
    elif selected_chord == "dom7":
        chord = ['X', '4', '3', '3', '2']
    elif selected_chord == "m7b5":
        chord = ['X', '3', '3', '4', '2']
    elif selected_chord == "dim":
        chord = ['X', '3', '3', '6']
    elif selected_chord == "aug":
        chord = ['X', '4', '4', '4']
    return chord

def get_progression(selected_progression):
    progression = []
    if selected_progression == "pop-punk":
        progression = [(0, 'I'), (7, 'V'), (9, 'vi'), (5, 'IV')]
    elif selected_progression == "blues-metal":
        progression = [(0, 'I'), (5, 'IV'), (0, 'I'), (7, 'V'), (5, 'IV'), (0, 'I')]
    elif selected_progression == "jazz_ii_v_i":
        progression = [(2, 'ii'), (7, 'V'), (0, 'I')]
    elif selected_progression == "doo_wop-Retro":
        progression = [(0, 'I'), (9, 'vi'), (5, 'IV'), (7, 'V')]
    elif selected_progression == "andalusian-descenso":
        progression = [(0, 'i'), (10, 'VII'), (8, 'VI'), (7, 'V')]
    elif selected_progression == "epic_minor":
        progression = [(0, 'i'), (8, 'VI'), (3, 'III'), (10, 'VII')]
    return progression

def get_strings(instrument):
    strings = 6
    if instrument == Instrument.Bass4 or instrument == Instrument.Bass4DropD or instrument == Instrument.Bass4DropC:
        strings = 4
    elif instrument == Instrument.Bass5:
        strings = 5
    elif instrument == Instrument.Guitar:
        strings = 6
    return strings

def home(request):
    instrument = Instrument.Bass4
    pattern = get_scale("mayor")
    managerTool = Manager(instrument)
    managerTool.set_strings_tool()
    managerTool.set_scale('A', pattern)
    raw_matrix = set_matrix(managerTool.tool_strings, instrument)
    string_names = list(reversed(managerTool.instrument))
    matrix = [{'name': name, 'cells': row} for name, row in zip(string_names, raw_matrix)]
    now_showing, instrument_label = build_now_showing('scale', 'A', 'mayor', 'major', 'pop-punk', 'bass4')
    return render(request, 'home.html', {
        'matrix': matrix,
        'string_names': string_names,
        'display_mode': 'degrees',
        'mode': 'scale',
        'scale': 'mayor',
        'chord': 'major',
        'progression': 'pop-punk',
        'key': 'A',
        'instrument': 'bass4',
        'now_showing': now_showing,
        'instrument_label': instrument_label,
    })


def button_action(request):
    selected_mode = "scale"
    selected_scale = "mayor"
    selected_chord = "major"
    selected_progression = "pop-punk"
    selected_key = "A"
    selected_instrument = "guitar"
    selected_display_mode = "degrees"
    
    if request.method == 'POST':
        selected_mode = request.POST.get('mode') if request.POST.get('mode') else "scale"
        selected_scale = request.POST.get('scale') if request.POST.get('scale') != "-1" else "mayor"
        selected_chord = request.POST.get('chord') if request.POST.get('chord') != "-1" else "major"
        selected_progression = request.POST.get('progression') if request.POST.get('progression') != "-1" else "pop-punk"
        selected_key = request.POST.get('key') if request.POST.get('key') != "-1" else "A"
        selected_instrument = request.POST.get('instrument') if request.POST.get('instrument') != "-1" else "guitar"
        selected_display_mode = request.POST.get('display_mode') if request.POST.get('display_mode') else "degrees"

        tool = Instrument.Guitar

        if selected_instrument == "bass4":
            tool = Instrument.Bass4
        elif selected_instrument == "bass4_drop_d":
            tool = Instrument.Bass4DropD
        elif selected_instrument == "bass4_drop_c":
            tool = Instrument.Bass4DropC
        elif selected_instrument == "bass5":
            tool = Instrument.Bass5
        elif selected_instrument == "guitar_drop_d":
            tool = Instrument.GuitarDropD
        elif selected_instrument == "guitar_half_step_down":
            tool = Instrument.GuitarHalfStepDown
        elif selected_instrument == "guitar_d_standard":
            tool = Instrument.GuitarDStandard
        elif selected_instrument == "guitar_drop_c":
            tool = Instrument.GuitarDropC
        elif selected_instrument == "guitar_dadgad":
            tool = Instrument.GuitarDADGAD
        elif selected_instrument == "guitar_open_g":
            tool = Instrument.GuitarOpenG
        elif selected_instrument == "guitar_open_d":
            tool = Instrument.GuitarOpenD
    else:
        tool = Instrument.Guitar

    if selected_mode == "scale":
        pattern = get_scale(selected_scale)
    elif selected_mode == "chord":
        pattern = get_chord(selected_chord)
    else:
        pattern = get_progression(selected_progression)

    managerTool = Manager(tool)
    managerTool.set_strings_tool()
    
    if selected_mode == "progression":
        managerTool.set_progression(selected_key, pattern)
    else:
        managerTool.set_scale(selected_key, pattern)  
    raw_matrix = set_matrix(managerTool.tool_strings, tool)
    string_names = list(reversed(managerTool.instrument))
    matrix = [{'name': name, 'cells': row} for name, row in zip(string_names, raw_matrix)]
    now_showing, instrument_label = build_now_showing(
        selected_mode, selected_key, selected_scale, selected_chord,
        selected_progression, selected_instrument)
    return render(request, 'home.html', {
        'matrix': matrix,
        'string_names': string_names,
        'mode': selected_mode,
        'scale': selected_scale,
        'chord': selected_chord,
        'progression': selected_progression,
        'key': selected_key,
        'instrument': selected_instrument,
        'display_mode': selected_display_mode,
        'now_showing': now_showing,
        'instrument_label': instrument_label,
    })


def set_matrix(tool_string, instrument):
    strings = get_strings(instrument)
    matrix = [[Note("") for j in range(13)] for i in range(strings)]
    for row_index, ts in enumerate(reversed(tool_string)):
        interval = 1
        for col_index, n in enumerate(ts):
            if col_index == 0 or n.step != 0:            
                matrix[row_index][col_index] = n

    return matrix