from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'recommender/home.html')

def about(request):
    return render(request, 'recommender/about.html')

def userEntered(request):
    return render(request, 'recommender/userEntered.html')

def follow(request):
    return render(request, 'recommender/follow.html')