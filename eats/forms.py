from django.forms import ModelForm
from eats.models import Business, tip

class edit_business_form(ModelForm):
    class Meta:
        model = Business
        exclude = ['description' , 'latitude', 'longitude']

class new_business_form(ModelForm):
    class Meta:
        model = Business
        exclude = ['description' , 'latitude', 'longitude']

class new_tip_form(ModelForm):
    class Meta:
        model = tip
        exclude = ['open_date']
