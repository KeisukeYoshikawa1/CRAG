from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import InputCrag
#from stock.forms import InputForm
from django.views.generic import FormView
#from stock.forms import ProductForm




def toppage(request):
    return render(request, 'toppage.html')

from stock.forms import InputCrag
def inputpage(request):
    form = InputCrag()
    return render(request, 'inputpage.html',{'form':form})



import googlemaps
import math
from googlemaps.places import places
import requests


def resultpage(request):
    form = InputCrag(request.POST)
    if form.is_valid():
        start_point_jp = form.cleaned_data.get('start_point_jp')
        input_distance_km = form.cleaned_data.get('input_distance_km')

        gmaps = googlemaps.Client(key="AIzaSyB-o7p9uyxwxAcSUYtpBzhHS3jaM2JuaBw")
        geocode_result = gmaps.geocode(start_point_jp)
        print(geocode_result)

        print(geocode_result[0]['geometry']['location']['lat'])
        print(geocode_result[0]['geometry']['location']['lng'])

        start_point_ll = [ geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng'] ]
        print(start_point_ll)


        c = {
            'start_point_ll': start_point_ll
            }

    return render(request, 'resultpage.html', c)


