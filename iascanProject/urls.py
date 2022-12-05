"""iascanProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from iascanApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name = "index"),
    path("portscan/", views.portScan, name = "portscan"),
    path("about/", views.about, name="about us"),
    path("portscan/startScan/",views.addScan, name ="start scan"),
    path("results/<int:id>", views.results, name ="results"),
    path("dirbuster/", views.dbuster, name ="dirbuster"),
    path("dirbresults/<int:id>", views.dirbresults, name ="dirbresults")
        # path("results/<int:id>", views.results, name ="results"),

    # path("details/<int:id>", views.details, name="details")
]
