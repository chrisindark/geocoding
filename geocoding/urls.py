from django.conf.urls import url
from .views import GeocodeCreateView


urlpatterns = [
    url(r'^$', GeocodeCreateView.as_view(), name='geocode_create'),
]
