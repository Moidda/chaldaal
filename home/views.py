from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

def home(request):
    return render(request, 'home_page.html')