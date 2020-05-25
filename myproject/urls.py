from django.contrib import admin
from django.urls import path

from eats import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home),
    path("debug/", views.debug),
    path("tips/", views.tips_main),
    path("manage/", views.eats_login),
    path("manage/main/", views.main),
    path("manage/main/logout/", views.eats_logout),
    path("manage/add_business/", views.add_business),
    path("manage/edit/biz/<int:biz_id>", views.edit_business),
    path("manage/add_vendor/$", views.add_vendor),
    path("manage/edit/vendor/<int:vendor_id>", views.edit_vendor),
    path("manage/tips/", views.tips_page),
    path("manage/tips/<int:tip_id>", views.edit_tips_page),
    path("manage/tips/reference_link/", views.ref_link_page),
    path("manage/tips/reference_link/<int:ref_id>", views.edit_ref_link_page),
]
