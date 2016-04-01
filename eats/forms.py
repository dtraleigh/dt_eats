from django.forms import ModelForm
from eats.models import Business, tip, reference_link

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

class edit_tip_form(ModelForm):
    class Meta:
        model = tip
        fields = '__all__'

class create_ref_link_form(ModelForm):
    class Meta:
        model = reference_link
        fields = '__all__'
