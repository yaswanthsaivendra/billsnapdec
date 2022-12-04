from django.urls import path, include
from . import views


urlpatterns = [
    path('addapp/', views.addapp, name='addapp'),
    path('editapp/<str:aslug>', views.editapp, name='editapp'),
    path('all/', views.showapps, name='showapps'),
    path('deleteapp/<aslug>',views.deleteapp,name='deleteapp'),
    path('remove-customer/<str:slug>/<str:userslug>',views.remove_user,name='remove-customer'),
    path('<slug>/', include('dashboard.urls')),
]