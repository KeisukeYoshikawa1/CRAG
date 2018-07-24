from django import forms
from stock.models import Crag

class InputCrag(forms.Form):
    start_point_jp = forms.CharField(label='スタート地点',widget=forms.TextInput(attrs={        'placeholder': '住所またはスポット名',    }))
    input_distance_km = forms.CharField(label='距離',widget=forms.TextInput(attrs={        'placeholder': '（例）40',    }))