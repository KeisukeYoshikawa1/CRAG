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



        c ={
            'start_point_ll':start_point_ll
            }

        # distance_diff_sort = sorted(distance_diff[1][0])
        # print( distance_diff_sort)


# mid_point_1 = [start_point_ll[0] , start_point_ll[1]+input_distance_ll[1]]
# mid_point_2 = [start_point_ll[0] + input_distance_ll[0] , start_point_ll[1]]
# mid_point_3 = [start_point_ll[0] , start_point_ll[1] - input_distance_ll[1]]
# mid_point_4 = [start_point_ll[0] - input_distance_ll[0] , start_point_ll[1]]
#
# print('point1','point2','point3','point4')
# print(mid_point_1,mid_point_2,mid_point_3,mid_point_4)

#     c = {
#         "start_point_jp": start_point_jp,
#         "input_distance_km": input_distance_km
#     }
    return render(request, 'resultpage.html', c)


