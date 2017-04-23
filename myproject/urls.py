from django.conf.urls import url
from django.contrib import admin
from eats import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^debug/$', views.debug),
    url(r'^tips/$', views.tips_main),
    url(r'^manage/$', views.eats_login),
    url(r'^manage/main/$', views.main),
    url(r'^manage/edit/(?P<biz_id>[0-9]+)$', views.edit_business),
    url(r'^manage/main/logout/$', views.eats_logout),
    url(r'^manage/add_business/$', views.add_business),
    url(r'^manage/tips/$', views.tips_page),
    url(r'^manage/tips/(?P<tip_id>[0-9]+)$', views.edit_tips_page),
    url(r'^manage/tips/reference_link/$', views.ref_link_page),
    url(r'^manage/tips/reference_link/(?P<ref_id>[0-9]+)$', views.edit_ref_link_page),
]
