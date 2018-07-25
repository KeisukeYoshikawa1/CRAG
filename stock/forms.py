from django import forms
from stock.models import Crag

class InputCrag(forms.Form):
    start_point_jp = forms.CharField(label='スタート地点',widget=forms.TextInput(attrs={        'placeholder': '住所またはスポット名',    }))
    input_distance_km = forms.IntegerField(label='距離（km）（数値のみ）' , min_value=0)