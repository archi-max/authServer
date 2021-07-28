
from .models import LicenseKey
from django.http import  HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

from datetime import datetime
import ntplib
import json
from .password_handler import PasswordManager, InvalidTokenError
import os
# Create your views here.

password = os.getenv("PASSWORD")



def get_time():
    curr_time = str(int(ntplib.NTPClient().request('time1.google.com', version=3).tx_time))
    return curr_time[:-2]+"00"

def decrypt(data):
    data = PasswordManager(get_time()+password).decrypt(data)
    return data

def encrypt(data):
    data = PasswordManager(get_time() + password).encrypt(data)
    return data

@csrf_exempt
def activity(request):
    if request.method != "POST":

        return HttpResponseNotAllowed(["GET"])
    try:
        data = json.loads(decrypt(request.body)).decode("utf-8")
    except InvalidTokenError:
        response = {"error": "Invalid Request"}
        return HttpResponse(encrypt(json.dumps(response)))
    activity_type = data['activity']

    try:
        obj = LicenseKey.objects.get(key=data['key'])
    except LicenseKey.DoesNotExist:
        response = {"error": "Invalid License Key"}
        return HttpResponse(encrypt(json.dumps(response)))

    if obj.active == False:
        response = {"error": "Key deactivated"}
        return HttpResponse(encrypt(json.dumps(response)))

    obj.last_activity = datetime.now()
    obj.save()

    if activity_type == "boot":

        obj.hardware_id = data['hardware_id']
        obj.save()

        response = "success"
        return HttpResponse(encrypt(json.dumps(response)))

    elif activity_type == "ping":
        if obj.hardware_id != data['hardware_id']:
            response = {"error": "multiple devices detected. permission denied!"}
            return HttpResponse(encrypt(json.dumps(response)))

        else:

            response = "success"
            return HttpResponse(encrypt(json.dumps(response)))

