from django.urls import path, include
from .views import *
from django.contrib.auth import views as a_views

app_name='groups'

urlpatterns = [
    path('panel/<str:slug>', groups_panel, name='groups-panel'),
    path('delete-group/<str:slug>/<str:appslug>', delete_group, name='delete-group'),
    path('group/<str:slug>', show_group, name='group'),
    path('add-member/<str:slug>', add_customer_to_group, name='add-member'),
    path('remove-member/<str:slug>', remove_customer_from_group, name='remove-member'),
    # path('update-group/<str:slug>/<str:groupslug>', update_user_group, name='update-group'),
    path('plangroup/<str:slug>', show_plan_group, name='plangroup'),

]