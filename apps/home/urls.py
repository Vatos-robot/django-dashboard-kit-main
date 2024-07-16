

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('commercial/', views.commercial_view, name='commercial'),
    path('comptable/', views.comptable_view, name='comptable'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
