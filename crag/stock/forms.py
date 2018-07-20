from django import forms
#from stock.models import Crag

class InputCrag(forms.Form):
    start_point_jp = forms.CharField(label='スタート地点')
    input_distance_km = forms.CharField(label='距離')