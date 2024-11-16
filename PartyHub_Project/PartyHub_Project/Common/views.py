from django.http import Http404
from django.shortcuts import render


# Create your views here.
def indexview(request):
    return render(request, 'Common/index.html')
