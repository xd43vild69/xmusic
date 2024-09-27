from django.shortcuts import render, redirect
from django.http import HttpResponse
from .manager import Manager

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
    m = Manager()

    string_6 = m.set_string("E")
    string_5 = m.set_string("A")
    string_4 = m.set_string("D")
    string_3 = m.set_string("G")
    string_2 = m.set_string("B")
    string_1 = m.set_string("E")

    for n in string_2:
        print(f"note : \033[31m{n.name}\033[0m")

    

