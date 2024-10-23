from django.shortcuts import render, redirect
from django.http import HttpResponse
from .manager.manager import Manager
from .instrument import Instrument
from .entities.note import Note

# Create your views here.

strings = 5

def get_scale(selected_scale):
    scale = []
    if selected_scale == "mayor":
        scale = ['H', 'W', 'W', 'H', 'W', 'W', 'W', 'H']
    elif selected_scale == "minor":
        scale = ['W', 'W', 'H', 'W', 'W', 'H', 'W', 'W']
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

def get_strings(instrument):
    strings = 6
    if instrument == Instrument.Bass4:
        strings = 4
    elif instrument == Instrument.Bass5:
        strings = 5
    elif instrument == Instrument.Guitar:
        strings = 6
    return strings

def home(request):
    instrument = Instrument.Bass4
    scale = get_scale("mayor")
    managerTool = Manager(instrument)
    managerTool.set_strings_tool()
    managerTool.set_scale('A', scale)
    matrix = set_matrix(managerTool.tool_strings, instrument)
    return render(request, 'home.html', {'matrix': matrix})


def button_action(request):
    selected_scale = None  # Default to None if nothing is selected yet
    
    if request.method == 'POST':
        # 'color' is the name of the select element
        selected_scale = request.POST.get('scale') if request.POST.get('scale') != "-1" else "mayor"                
        selected_key = request.POST.get('key') if request.POST.get('key') != "-1" else "A"                
        selected_instrument = request.POST.get('instrument') if request.POST.get('instrument') != "-1" else "guitar"

        tool = Instrument.Guitar

        if selected_instrument == "bass4":
            tool = Instrument.Bass4
        elif selected_instrument == "bass5":
            tool = Instrument.Bass5

    scale = get_scale(selected_scale)
    managerTool = Manager(tool)
    managerTool.set_strings_tool()
    managerTool.set_scale(selected_key, scale)  
    matrix = set_matrix(managerTool.tool_strings, tool)
    return render(request, 'home.html', {'matrix': matrix, 'scale' : selected_scale, 'key' : selected_key, 'instrument' : selected_instrument})


def set_matrix(tool_string, instrument):
    strings = get_strings(instrument)
    matrix = [[Note("") for j in range(13)] for i in range(strings)]
    for row_index, ts in enumerate(reversed(tool_string)):
        interval = 1
        for col_index, n in enumerate(ts):

            if n.step != 0:            
                matrix[row_index][col_index] = n
                interval += 1

            if interval > 8:
                break

    return matrix

def set_chords(chords):
    matrix = [[Note("") for j in range(13)] for i in range(6)]

    for c in chords:
        matrix[c.string][c.fret] = c.note
    
    return matrix

def set_chord(name):
    locations = []
    if name == "c1":
        locations = [[6,0],[5,2], [4,2], [3,3], [2,0], [1,0]]
    
    return locations