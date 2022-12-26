"""TPproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from TPapp import views, api
from TPapp.views import graph_all, graph_24h, graph_mois, graph_heure, Temp_serializer_agregar_data, menu, psg, \
    export_xls, test

urlpatterns = [
    path('', menu, name='home'),
    path('api/list',api.Dlist,name='DHT11List'),
    path('api/post',api.Dsviews.as_view(),name='DHT_post'),
    path("graph_24h",graph_24h,name="jours"),
    path("graph_all",graph_all,name="alldata"),
    path("graph_mois",graph_mois,name="mois"),
    path("graph_heure",graph_heure,name="heure"),
    path("snippets/",Temp_serializer_agregar_data,name="liste"),
    path("psg",psg,name="psg"),
    url(r'^export/xls/$', export_xls, name='export_xls'),
    path('report', views.report),
]
