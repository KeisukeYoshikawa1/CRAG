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

def resultpage(request):
    form = InputCrag(request.POST)
    if form.is_valid():
        start_point_jp = form.cleaned_data.get('start_point_jp')
        input_distance_km = form.cleaned_data.get('input_distance_km')


    c = {
        "start_point_jp": start_point_jp,
        "input_distance_km": input_distance_km
    }
    return render(request, 'resultpage.html', c)


