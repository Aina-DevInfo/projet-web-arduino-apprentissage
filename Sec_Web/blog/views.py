from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
import numpy as np


import os
from joblib import load
import pandas as pd

import  pyrebase


config = {
    "apiKey": "AIzaSyCNyiQqFqFN5jvo4uOadMUwt2y1Ml7LHgE",
    "authDomain": "dht22-2b353.firebaseapp.com",
    "databaseURL": "https://dht22-2b353-default-rtdb.firebaseio.com",
    "projectId": "dht22-2b353",
    "storageBucket": "dht22-2b353.appspot.com",
    "messagingSenderId": "422339478465",
    "appId": "1:422339478465:web:74a0393d617bb8b519a540"
}



firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Create your views here.


def premierPage(request):
    humidity = database.child('dht22').child('Humidity').get().val()
    temperature = database.child('dht22').child('Temperature').get().val()
    print(humidity)
    return render(request, "index.html", {"humidity": humidity, "temperature": temperature})

class NewProduct(View):

    def get(self, request):
        humidity = database.child('dht22').child('Humidity').get().val()
        temperature = database.child('dht22').child('Temperature').get().val()
        
        
        context = {'hum': humidity, 'temp':temperature }
        return JsonResponse(context)
    

class NewPred(View):
    def get(self, request):
        #####
        modele_dir = 'blog/modele'

        fichier_temp = os.path.join(modele_dir, 'modele_temperature.pkl')
        fichier_hum = os.path.join(modele_dir, 'modele_Humidite.pkl')

        modele_temp = load(fichier_temp)
        modele_hum = load(fichier_hum)

        humidity = database.child('dht22').child('Humidity').get().val()
        temperature = database.child('dht22').child('Temperature').get().val()
        temp = np.array([[temperature]])
        hum = np.array([[humidity]])

        temperature_predite = modele_temp.predict(temp)
        print(type(temperature_predite))
        print(f"Température prédite : {temperature_predite[0]}")

        humidite_predite = modele_hum.predict(hum)
        print(f"Humidité prédite : {humidite_predite[0]}")

        #####
        context = {'hum2': humidite_predite[0], 'temp2': temperature_predite[0] }
        return JsonResponse(context)