from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id_report>/', views.manual_paginating, name='manual_paginating'),
    path('default/', views.default_paginating, name='default_paginating'),
]