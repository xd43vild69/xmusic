from django.shortcuts import render, redirect
from django.http import HttpResponse
from .manager import Manager
from .instrument import Instrument
from .note import Note

# Create your views here.


def home(request):

    scale = ['W', 'W', 'H', 'W', 'W', 'H', 'W', 'W']
    managerTool = Manager(Instrument.Guitar)
    managerTool.set_strings_tool()
    managerTool.set_scale('E', scale)

    matrix = set_matrix(managerTool.tool_strings)
    # m = managerTool.tool_strings

    # return render(request, 'matrix.html', {'matrix': matrix})
    return render(request, 'home.html', {'matrix': matrix})


def set_matrix(tool_string):
    matrix = [[Note("") for j in range(13)] for i in range(6)]
    interval = 1
    for i1, ts in enumerate(reversed(tool_string)):
        for i2, n in enumerate(ts):

            if n.step != 0:
                print(f"{n.name} is {n.step}")
                matrix[i1][i2] = n
                interval +=1 

            if interval > 8:
                interval = 1
                break          

    return matrix


def button_action(request):
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
