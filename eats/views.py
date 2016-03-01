from django.shortcuts import render
from eats.models import Business, District

def home(request):
    #///
    #Create the list of businesses that should be shown on the main site and  the districts
    #\\\
    business_list = Business.objects.filter(display_on_site=True).order_by('name')
    district_list = District.objects.all().order_by('name')

    #Need to build an array of arrays that contain the district and the appropriate eats, drinks,
    #coffees labels, depending on if these are appropriate or not.
    #
    #labels_array = [[4, "Eats", "Drinks", "Coffees"],
    #                [2, "Eats", "Coffees"]]

    labels_array = []

    for district in district_list:
        new_district_array = []
        new_district_array.append(district.id)
        for business in business_list:
            if business.is_eats and business.district == district and business.display_on_site:
                new_district_array.append("Eats")
                break
        for business in business_list:
            if business.is_drinks and business.district == district and business.display_on_site:
                new_district_array.append("Drinks")
                break
        for business in business_list:
            if business.is_coffee and business.district == district and business.display_on_site:
                new_district_array.append("Coffees")
                break
        labels_array.append(new_district_array)

    return render(request, 'index.html',
                  {'business_list': business_list,
                   'district_list' : district_list,
                   'labels_array' : labels_array})
