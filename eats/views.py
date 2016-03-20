from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from eats.models import Business, District
from eats.forms import edit_business_form, new_business_form
import datetime

def home(request):
    #///
    #Create the list of businesses that should be shown on the main site and the districts
    #\\\
    district_list = District.objects.all().order_by('name')

    #Get only open businesses.
    open_businesses = Business.objects.filter(
                Q(open_date__lte=datetime.datetime.today()) &
                (Q(close_date=None) | Q(close_date__gt=datetime.datetime.today()))
            ).order_by('name')

    #Need to build an array of arrays that contain the district and the appropriate eats, drinks,
    #coffees labels, depending on if these are appropriate or not.
    #
    #labels_array = [[4, "Eats", "Drinks", "Coffees"],
    #                [2, "Eats", "Coffees"]]

    labels_array = []

    for district in district_list:
        new_district_array = []
        new_district_array.append(district.id)
        for business in open_businesses:
            if business.is_eats and business.district == district:
                new_district_array.append("Eats")
                break
        for business in open_businesses:
            if business.is_drinks and business.district == district:
                new_district_array.append("Drinks")
                break
        for business in open_businesses:
            if business.is_coffee and business.district == district:
                new_district_array.append("Coffees")
                break
        labels_array.append(new_district_array)

    return render(request, 'index.html',
                  {'business_list': open_businesses,
                   'district_list' : district_list,
                   'labels_array' : labels_array})

def eats_login(request):
    #///
    #This is the login page for the management view. (not the django admin page)
    #\\\
    message = 'Please log in'

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                message = 'Login successful.'

                return HttpResponseRedirect('/manage/main/')
            else:
                message = 'Account is disabled.'
        else:
            message = 'Invalid login.'

    return render(request, 'login.html', {'message':message})

def eats_logout(request):
    logout(request)

    return HttpResponseRedirect('/manage/')

@login_required(login_url='/manage/')
def main(request):
    #///
    #This is the main manage page.
    #\\\
    all_businesses = Business.objects.all()

    return render(request, 'main.html', {'all_businesses':all_businesses})

@login_required(login_url='/manage/')
def edit_business(request, biz_id):
    #///
    #This page should show the edit business form
    #\\\
    business_to_edit = Business.objects.get(id=biz_id)

    if request.POST:
        form = edit_business_form(request.POST, instance=business_to_edit)

        if "cancel-button" in request.POST:
            messages.info(request, 'Canceled edit to ' + business_to_edit.name + '.')

            return HttpResponseRedirect('/manage/main/')

        if form.is_valid():
            form.save()
            messages.success(request, 'Details for ' + business_to_edit.name + ' updated.')

            return HttpResponseRedirect('/manage/main/')

    form = edit_business_form(initial=
        {'name': business_to_edit.name,
        'district': business_to_edit.district,
        'link': business_to_edit.link,
        'has_outdoor_seating': business_to_edit.has_outdoor_seating,
        'is_temp_closed': business_to_edit.is_temp_closed,
        'is_eats': business_to_edit.is_eats,
        'is_drinks': business_to_edit.is_drinks,
        'is_coffee': business_to_edit.is_coffee,
        'not_local': business_to_edit.not_local,
        'close_date': business_to_edit.close_date,
        'open_date': business_to_edit.open_date}
        )

    return render(request, 'business_edit.html', {'form':form})

@login_required(login_url='/manage/')
def add_business(request):
    #///
    #This page has a form for adding a new business.
    #\\\
    if request.POST:
        form = edit_business_form(request.POST)

        if "cancel-button" in request.POST:
            messages.info(request, 'Canceled adding new business.')

            return HttpResponseRedirect('/manage/main/')

        if form.is_valid():
            new_business_name = form.cleaned_data['name']
            form.save()
            messages.success(request, 'New business, ' + new_business_name + ', added.')

            return HttpResponseRedirect('/manage/main/')

    form = new_business_form()

    return render(request, 'business_add.html', {'form':form})

@login_required(login_url='/manage/')
def tips_page(request, biz_id):
    #///
    #This page shows and manages all the tips.
    #\\\

    pass
