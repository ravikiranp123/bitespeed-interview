import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from .recon_logic import recon_main

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def identify(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body['email']
        phoneNumber = body['phoneNumber']
        res = recon_main(email, phoneNumber)
        return HttpResponse(json.dumps(res))
    return HttpResponseNotFound("Only post methods are accepted")