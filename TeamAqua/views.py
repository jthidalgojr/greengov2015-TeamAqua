from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from api.soql import *

# Create your views here.

def indexView(request):
    return render(request,'TeamAqua/index.html' )
