from django.urls import path

from . import views

app_name = "listings"

urlpatterns = [
    path("<str:item_id>", views.listing, name="listing")
]
