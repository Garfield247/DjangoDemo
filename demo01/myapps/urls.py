from django.conf.urls import url
from myapps import views

urlpatterns = [
    url(r'^$',views.welcome),
    url(r'^template_test/$',views.template_test),
    url(r'^model_test/$',views.model_test),
]