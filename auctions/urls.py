from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<str:listing_id>", views.listing_page, name="listing_page"),
]
