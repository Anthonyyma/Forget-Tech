from django.http import request
from django.shortcuts import render
from requests.api import get
from .models import Activities, States
import requests, json, os

activity = ''
# Create your views here.
def index(response):

    # f = open('main/t.txt', 'r')
    # l = f.readlines()

    # for line in l:
    #     g = line.split('\t')
    #     print(g[0], g[2])
    #     States(name=g[0], abv=g[2]).save()

    names = []
    descriptions = []
    images = []
    codes = []
    lists = []
    
    states = States.objects.all
    activities = Activities.objects.all


    if response.method == "POST":
        global activity

        getActivity = response.POST.getlist('activityResult')[0]
        activity = getActivity
        getState = States.objects.filter(name=response.POST.getlist('stateResult')[0])[0].abv

        npsAPI = os.environ.get('NPSAPI')

        address = 'https://developer.nps.gov/api/v1/' + getActivity + '?q=' + getState + '&api_key=' + npsAPI

        r = requests.get(address)
        j = json.loads(r.text)

        for i in range(len(j.get('data'))):
            if len(j.get('data')[i].get('images')) != 0:
                if j.get('data')[i].get('images')[0].get('url') is not None:
                    img = j.get('data')[i].get('images')[0].get('url')
                    images.append(img)

                    name = j.get('data')[i].get('fullName')
                    if name is None:
                        name = j.get('data')[i].get('name')
                    names.append(name)

                    desc = j.get('data')[i].get('description')
                    descriptions.append(desc)

                    code = j.get('data')[i].get('parkCode')
                    codes.append(code)

        lists = zip(names, descriptions, images, codes)

    return render(response, 'main/index.html', {'states':states, 'activities':activities, 'lists':lists})

def info(response):
    activities = []
    googleAPI = os.environ.get('GOOGLEAPI')

    #get info of chosen location
    code = response.GET.get('code')
    npsAPI = os.environ.get('NPSAPI')
    address = 'https://developer.nps.gov/api/v1/' + activity + '?parkCode=' + code + '&api_key=' + npsAPI

    r = requests.get(address)
    j = json.loads(r.text)
    print(activity)
    
    if 'Parks' in activity:
        for i in range(len(j.get('data')[0].get('activities'))):
            activities.append(j.get('data')[0].get('activities')[i].get('name'))    


    img = j.get('data')[0].get('images')[0].get('url')

    title = j.get('data')[0].get('fullName')
    if title is None:
        title = j.get('data')[0].get('name')

    desc = j.get('data')[0].get('description')

    lat = j.get('data')[0].get('latitude')

    lng = j.get('data')[0].get('longitude')

    contact = j.get('data')[0].get('contacts').get('phoneNumbers')[0].get('phoneNumber')

    hours = j.get('data')[0].get('operatingHours')[0].get('description')

    weatherAPI = os.environ.get('WEATHERAPI')

    #get weather of chosen location
    address = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lng + '&units=metric&exclude=hourly,minutely,daily&appid=' + weatherAPI

    r = requests.get(address)
    j = json.loads(r.text)

    temp = j.get('current').get('temp')
    tempf = temp * 9 // 5 + 32
    tempDesc = j.get('current').get('weather')[0].get('description')

    return render(response, 'main/info.html', {'title':title, 'desc':desc, 'img':img, 'lat':lat, 'lng':lng, 'temp':temp, 'tempf':tempf, 'tempDesc':tempDesc, 'activities':activities, 'googleAPI':googleAPI, 'contact':contact, 'hours':hours})