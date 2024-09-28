from django.shortcuts import render, redirect
from django.http import HttpResponse
from .manager import Manager
from .instrument import Instrument
from .note import Note

# Create your views here.


def get_scale(selected_scale):
    scale = []
    if selected_scale == "s1":
        scale = ['H', 'W', 'W', 'H', 'W', 'W', 'W', 'H']
    elif selected_scale == "s2":
        scale = ['W', 'W', 'H', 'W', 'W', 'H', 'W', 'W']
    return scale

def home(request):

    scale = get_scale("s1")
    managerTool = Manager(Instrument.Guitar)
    managerTool.set_strings_tool()
    managerTool.set_scale('E', scale)
    matrix = set_matrix(managerTool.tool_strings)
    return render(request, 'home.html', {'matrix': matrix})

def button_action(request):
    selected_scale = None  # Default to None if nothing is selected yet

    if request.method == 'POST':
        selected_scale = request.POST.get('scale')  # 'color' is the name of the select element
        selected_key = request.POST.get('key')

    scale = get_scale(selected_scale)
    managerTool = Manager(Instrument.Guitar)
    managerTool.set_strings_tool()
    managerTool.set_scale(selected_key, scale)
    matrix = set_matrix(managerTool.tool_strings)

    return render(request, 'home.html', {'matrix': matrix})

def set_matrix(tool_string):
    matrix = [[Note("") for j in range(13)] for i in range(6)]
    for row_index, ts in enumerate(reversed(tool_string)):
        interval = 1
        for col_index, n in enumerate(ts):

            if n.step != 0:
                print(f"{n.name} is {n.step}")
                matrix[row_index][col_index] = n
                interval +=1 

            if interval > 8:
                break          

    return matrix


def button_action2(request):
    if request.method == "POST":
        # Perform your server-side action here
        # Example: Print a message, update the database, etc.
        # print("Button clicked!")
        call_manager()

        # You can return a response or redirect to another page
        return HttpResponse("Button was clicked and action performed!")
    else:
        # Redirect or return an error if this URL is accessed without a POST request
        return redirect('/')


def call_manager():
    managerTool = Manager(Instrument.Guitar)
    managerTool.set_strings_tool()

    # scale = ['H', 'W', 'W', 'H', 'W', 'W', 'W', 'H']
    scale = ['W', 'W', 'H', 'W', 'W', 'H', 'W', 'W']

    managerTool.set_scale('E', scale)

    for s in managerTool.tool_strings:
        print("string")
        for n in s:
            if n.step != 0:
                print(f"{n.name} is {n.step}")
