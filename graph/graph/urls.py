"""graph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from twitter_mining import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.twitter_name),
    url(r'^index123/',views.twitter_name_chart,name='submitdata'),
    url(r'^tweet/',views.twitter_name_list,name='submitdata2'),
    url(r'^user/',views.twitter_name_user,name='submitdata3'),
    url(r'^city/',views.twitter_city_list,name="fullcity"),
    url(r'^crime/',views.twitter_crime_list,name="fullcity"),
    url(r'^crime-city/',views.twitter_crime_chart,name="submitdata4"),
    url(r'^time-series/',views.time_series,name="asd"),



]
