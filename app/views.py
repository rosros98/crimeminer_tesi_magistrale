from django.shortcuts import render
import csv 

# Create your views here.
def app(request):
    return render(request, 'dashboard.html')

def individualWiretaps(request):
    return render(request, 'features/individualWiretaps.html')

def individualCrimes(request):
    return render(request, 'features/individualCrimes.html')

def individualEnviromentalTapping(request):
    return render(request, 'features/individualEnviromentalTapping.html')

def individualCrimesEnviromentalTapping(request):
    return render(request, 'features/individualCrimesEnviromentalTapping.html')

def interlocutoreCrimes(request):
    return render(request, 'features/interlocutoreCrimes.html')