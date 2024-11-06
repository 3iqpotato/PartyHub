from django.http import Http404
from django.shortcuts import render

# Create your views here.
def indexview(request):

    # return render(request, '404.html', status=404)
    # return render(request, 'Party/event_list.html')

    return render(request, 'Common/index.html')