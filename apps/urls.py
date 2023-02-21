from django.urls import path, include
from . import views


urlpatterns = [
    path('addbillingapp/', views.addbillingapp, name='addbillingapp'),
    path('addnonbillingapp/', views.addnonbillingapp, name='addnonbillingapp'),
    path('editapp/<str:aslug>', views.editapp, name='editapp'),
    path('all/', views.showapps, name='showapps'),
    path('deleteapp/<aslug>',views.deleteapp,name='deleteapp'),
    path('remove-customer/<str:slug>/<str:userslug>',views.remove_user,name='remove-customer'),
    path('<slug>/', include('dashboard.urls')),
]