import django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from eats.models import *
from eats.forms import *
import datetime
from itertools import chain


def debug(request):
    version = str(django.VERSION)

    return render(request, 'debug.html', {'version': version})


def home(request):
    # ///
    # Create the list of businesses that should be shown on the main site and the districts
    # \\\
    district_list = District.objects.all().order_by('name')

    # Get only open businesses. Basically, if it has a closing date equal or lt today, it's open or coming soon.
    open_and_coming_soon_businesses = Business.objects.filter(~Q(close_date__lt=datetime.datetime.today())).order_by('name')

    # Get only open Vendors. Basically, if it has a closing date equal or lt today, it's open or coming soon.
    open_and_coming_soon_vendors = Vendor.objects.filter(
        Q(open_date__lte=datetime.datetime.today()) &
        (Q(close_date=None) | Q(close_date__gt=datetime.datetime.today()))
    ).order_by('name')

    # Need to build an array of arrays that contain the district and the appropriate eats, drinks,
    # coffees labels, depending on if these are appropriate or not.
    #
    # labels_array = [[4, 'Eats', 'Drinks', 'Coffees'],
    #                [2, 'Eats', 'Coffees']]

    labels_array = []

    for district in district_list:
        new_district_array = []
        new_district_array.append(district.id)
        for business in open_and_coming_soon_businesses:
            if business.is_eats and business.district == district:
                new_district_array.append('Eats')
                break
        for business in open_and_coming_soon_businesses:
            if business.is_drinks and business.district == district:
                new_district_array.append('Drinks')
                break
        for business in open_and_coming_soon_businesses:
            if business.is_coffee and business.district == district:
                new_district_array.append('Coffees')
                break
        labels_array.append(new_district_array)

    return render(request, 'index.html',
                  {'business_list': open_and_coming_soon_businesses,
                   'vendor_list': open_and_coming_soon_vendors,
                   'district_list': district_list,
                   'labels_array': labels_array})


def tips_main(request):
    # ///
    # Page for showing tips to visitors
    # \\\
    all_tips = tip.objects.filter((Q(open_date=None) |
                                Q(open_date__gt=datetime.datetime.today())) &
                                Q(added=False)).order_by('-date')
    today = datetime.date.today()

    return render(request, 'tips_main.html', {'all_tips': all_tips,
                                              'today': today})


def eats_login(request):
    # ///
    # This is the login page for the management view. (not the django admin page)
    # \\\
    message = 'Log in'

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
    # ///
    # This is the main manage page.
    # \\\
    all_businesses = Business.objects.all().order_by('-date_added')
    all_vendors = Vendor.objects.all().order_by('-date_added')
    all_places = sorted(chain(all_businesses, all_vendors), key=lambda place: place.date_added, reverse=True)

    recent_snapshot = snapshot.objects.latest('date')

    total_open = recent_snapshot.local_business_count + recent_snapshot.not_local_business_count

    local_percent = (recent_snapshot.local_business_count / total_open) * 100

    return render(request, 'main.html', {'all_places': all_places,
                                         'recent_snapshot': recent_snapshot,
                                         'local_percent': round(local_percent, 1)})


@login_required(login_url='/manage/')
def add_business(request):
    # ///
    # This page has a form for adding a new business.
    # \\\
    if request.method == 'POST':
        form = edit_business_form(request.POST)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled adding new business.')

            return HttpResponseRedirect('/manage/main/')

        if form.is_valid():
            new_business_name = form.cleaned_data['name']
            form.save()
            messages.success(request, 'New business, ' + new_business_name + ', added.')

            return HttpResponseRedirect('/manage/main/')
    else:
        # form = new_business_form(initial={'link': 'http://', })
        form = new_business_form()

    return render(request, 'business_add.html', {'form': form})


@login_required(login_url='/manage/')
def edit_business(request, biz_id):
    # ///
    # This page should show the edit business form
    # \\\
    business_to_edit = Business.objects.get(id=biz_id)

    if request.method == 'POST':
        form = edit_business_form(request.POST, instance=business_to_edit)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled edit to ' + business_to_edit.name + '.')

            return HttpResponseRedirect('/manage/main/')

        if form.is_valid():
            form.save()
            messages.success(request, 'Details for ' + business_to_edit.name + ' updated.')

            if 'save-logout-button' in request.POST:
                return HttpResponseRedirect('/manage/main/logout/')
            else:
                return HttpResponseRedirect('/manage/main/')
    else:
        form = edit_business_form(instance=business_to_edit)

    return render(request, 'business_edit.html', {'form': form})


@login_required(login_url='/manage/')
def add_vendor(request):
    # ///
    # This page has a form for adding a new vendor.
    # \\\
    if request.method == 'POST':
        form = edit_vendor_form(request.POST)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled adding new vendor.')

            return HttpResponseRedirect('/manage/main/')

        if form.is_valid():
            new_vendor_name = form.cleaned_data['name']
            form.save()
            messages.success(request, 'New vendor, ' + new_vendor_name + ', added.')

            return HttpResponseRedirect('/manage/main/')
    else:
        # form = new_vendor_form(initial={'link': 'http://', })
        form = new_vendor_form()
        form.fields['food_hall'].queryset = Business.objects.filter(is_food_hall=True)

    return render(request, 'vendor_add.html', {'form': form})


@login_required(login_url='/manage/')
def edit_vendor(request, vendor_id):
    # ///
    # This page should show the edit vendor form
    # \\\
    vendor_to_edit = Vendor.objects.get(id=vendor_id)

    if request.method == 'POST':
        form = edit_vendor_form(request.POST, instance=vendor_to_edit)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled edit to ' + vendor_to_edit.name + '.')

            return HttpResponseRedirect('/manage/main/')

        if form.is_valid():
            form.save()
            messages.success(request, 'Details for ' + vendor_to_edit.name + ' updated.')

            if 'save-logout-button' in request.POST:
                return HttpResponseRedirect('/manage/main/logout/')
            else:
                return HttpResponseRedirect('/manage/main/')
    else:
        form = edit_vendor_form(instance=vendor_to_edit)
        form.fields['food_hall'].queryset = Business.objects.filter(is_food_hall=True)

    return render(request, 'vendor_edit.html', {'form': form})


@login_required(login_url='/manage/')
def tips_page(request):
    # ///
    # This page shows and manages all the tips.
    # \\\
    tip_list = tip.objects.all()
    district_list = District.objects.all()
    today = datetime.date.today()
    open_businesses = Business.objects.filter(Q(open_date__lte=datetime.datetime.today()) &
                (Q(close_date=None) | Q(close_date__gt=datetime.datetime.today()))
            )

    # Update our tips 'added' field. If there is an open business with the same name as the tip,
    # I'll assume that I've already added it from the tip list.
    # for business in open_businesses:
    #     for a_tip in tip_list:
    #         if business.name == a_tip.name:
    #             a_tip.added = True
    #             a_tip.save()

    if request.method == 'POST':
        tip_form = new_tip_form(request.POST)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled adding new tip.')

            return HttpResponseRedirect('/manage/tips/')

        if tip_form.is_valid():
            new_tip_name = tip_form.cleaned_data['name']
            tip_form.save()
            messages.success(request, 'New tip, ' + new_tip_name + ', added.')

            return HttpResponseRedirect('/manage/tips/')
    else:
        tip_form = new_tip_form()
        tip_form.fields['food_hall'].queryset = Business.objects.filter(is_food_hall=True)

    return render(request, 'tips.html', {'tip_list': tip_list,
                                         'district_list': district_list,
                                         'tip_form': tip_form,
                                         'today': today,
                                         'open_businesses': open_businesses})


@login_required(login_url='/manage/')
def edit_tips_page(request, tip_id):
    the_tip = tip.objects.get(id=tip_id)

    if request.method == 'POST':
        tip_form = edit_tip_form(request.POST, instance=the_tip)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled editing the tip.')

            return HttpResponseRedirect('/manage/tips/')

        if 'delete-button' in request.POST:
            the_tip.delete()
            messages.info(request, 'Tip has been deleted.')

            return HttpResponseRedirect('/manage/tips/')

        if tip_form.is_valid():
            tip_form.save()

            if 'create-biz' in request.POST:
                new_biz = Business.objects.create(name=the_tip.name,
                                                  district=the_tip.district,
                                                  link=the_tip.link,
                                                  description=the_tip.description,
                                                  has_outdoor_seating=the_tip.has_outdoor_seating,
                                                  is_temp_closed=the_tip.is_temp_closed,
                                                  is_eats=the_tip.is_eats,
                                                  is_drinks=the_tip.is_drinks,
                                                  is_coffee=the_tip.is_coffee,
                                                  not_local=the_tip.not_local,
                                                  open_date=the_tip.open_date)
                the_tip.added = True
                the_tip.save()

                messages.info(request, 'New business ' + new_biz.name + ' created.')

            if 'create-vendor' in request.POST:
                new_vendor = Vendor.objects.create(name=the_tip.name,
                                                   food_hall=the_tip.food_hall,
                                                   link=the_tip.link,
                                                   description=the_tip.description,
                                                   is_temp_closed=the_tip.is_temp_closed,
                                                   not_local=the_tip.not_local,
                                                   open_date=the_tip.open_date)
                the_tip.added = True
                the_tip.save()

                messages.info(request, 'New vendor ' + new_vendor.name + ' created.')

            messages.success(request, 'Tip, ' + the_tip.name + ', edited.')

            return HttpResponseRedirect('/manage/tips/')
    else:
        tip_form = edit_tip_form(instance=the_tip)
        tip_form.fields['food_hall'].queryset = Business.objects.filter(is_food_hall=True)

    return render(request, 'edit_tips.html', {'tip_form': tip_form})


@login_required(login_url='/manage/')
def ref_link_page(request):
    ref_link_list = reference_link.objects.all().order_by('-date_created')

    if request.method == 'POST':
        link_form = create_ref_link_form(request.POST)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled creating reference link.')

            return HttpResponseRedirect('/manage/tips/')

        if link_form.is_valid():
            new_headline = link_form.cleaned_data['headline']
            link_form.save()
            messages.success(request, 'Reference Link, ' + new_headline + ', added.')

            if 'save-and-add' in request.POST:
                return HttpResponseRedirect('/manage/tips/reference_link/')
            else:
                return HttpResponseRedirect('/manage/tips/')

    else:
        link_form = create_ref_link_form()

    return render(request, 'ref_link.html', {'ref_link_list': ref_link_list,
                                             'link_form': link_form})


@login_required(login_url='/manage/')
def edit_ref_link_page(request, ref_id):
    ref_link = reference_link.objects.get(id=ref_id)

    if request.method == 'POST':
        link_form = create_ref_link_form(request.POST, instance=ref_link)

        if 'cancel-button' in request.POST:
            messages.info(request, 'Canceled editing reference link.')

            return HttpResponseRedirect('/manage/tips/reference_link/')

        if link_form.is_valid():
            new_headline = link_form.cleaned_data['headline']
            link_form.save()
            messages.success(request, 'Reference Link, ' + new_headline + ', edited.')

            return HttpResponseRedirect('/manage/tips/reference_link/')

    else:
        link_form = create_ref_link_form(initial={'url_link': ref_link.url_link,
                                                  'description': ref_link.description,
                                                  'headline': ref_link.headline,
                                                  'date_published': ref_link.date_published
        })

    return render(request, 'edit_ref_link.html', {'ref_link': ref_link,
                                                  'link_form': link_form})