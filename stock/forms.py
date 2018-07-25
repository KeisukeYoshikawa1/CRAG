from django import forms
from stock.models import Crag

class InputCrag(forms.Form):
    start_point_jp = forms.CharField(required=True,label='スタート地点',widget=forms.TextInput(attrs={        'placeholder': '住所またはスポット名', 'style':'font-size:30px;'   }))
    input_distance_km = forms.IntegerField(required=True, label='距離（km）' , widget=forms.TextInput(attrs={        'placeholder': '数値のみ', 'style':'font-size:30px;'   }) )