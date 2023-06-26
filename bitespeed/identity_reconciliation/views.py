import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from .recon_logic import recon_main
from .models import User
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

@csrf_exempt
def reset(request):
    if request.method == "POST":
        User.objects.filter(linkPrecedence=User.LinkPrecedenceChoices.secondary).delete()
        User.objects.filter(linkPrecedence=User.LinkPrecedenceChoices.primary).delete()
        return HttpResponseNotFound("Success")
    return HttpResponseNotFound("Only post methods are accepted")