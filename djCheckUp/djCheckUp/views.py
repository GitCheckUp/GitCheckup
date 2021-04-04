from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'djCheckUp/homepage.html')

def showMessage(request):
    return HttpResponse("Analyzed.")
