

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.home,name="home"),
    path('index/', views.index, name='direction'),
    path('commercial/', views.commercial_view, name='commercial'),
    path('comptable/', views.comptable_view, name='comptable'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
