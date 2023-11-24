from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from models.common.edsr import model

# Create your views here.

@require_http_methods(['POST'])
def edsr(request):
    b64 = request.POST["source"]
    
    return HttpResponse("u r right")