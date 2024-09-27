from django.shortcuts import render, redirect
from django.http import HttpResponse
from .manager import Manager
from .instrument import Instrument


# Create your views here.
def home(request):
    matrix = [[(i * 12) + j + 1 for j in range(12)] for i in range(6)]
    #return render(request, 'matrix.html', {'matrix': matrix})
    return render(request, 'home.html', {'matrix': matrix})


def button_action(request):
    if request.method == "POST":
        # Perform your server-side action here
        # Example: Print a message, update the database, etc.
        #print("Button clicked!")
        call_manager()

        # You can return a response or redirect to another page
        return HttpResponse("Button was clicked and action performed!")
    else:
        # Redirect or return an error if this URL is accessed without a POST request
        return redirect('/')
    
def call_manager():
    managerTool = Manager(Instrument.Guitar)
    managerTool.set_strings_tool()

    #scale = ['H', 'W', 'W', 'H', 'W', 'W', 'W', 'H']
    scale = ['W', 'W', 'H', 'W', 'W', 'H', 'W', 'W']
    
    tool =  managerTool.set_scale('A', scale)
    
    for s in managerTool.tool_strings:
        print("string")
        for n in s:            
            if n.step != 0:
                print(f"{n.name} is {n.step}")
    

