from django.shortcuts import render
from django.http import HttpResponse
#clientid x8fg722d4g22ulw5aqvcvbi5w3vaca
def index(request):
    return render(request, 'index.html')