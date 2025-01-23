from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants'] # exclude these fields from the form fields              