from django.forms import ModelForm
from eats.models import Business

class edit_business_form(ModelForm):
    class Meta:
        model = Business
        exclude = ['description' , 'latitude', 'longitude']

class new_business_form(ModelForm):
    class Meta:
        model = Business
        exclude = ['description' , 'latitude', 'longitude']
