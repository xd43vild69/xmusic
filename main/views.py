from django.shortcuts import render, redirect
from django.http import HttpResponse
from .manager import Manager
from .instrument import Instrument


# Create your views here.
def home(request):
    return render(request, 'home.html')


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
    tool = managerTool.set_strings_tool()
    managerTool.set_scale('E')
    n1 = "x"
    

