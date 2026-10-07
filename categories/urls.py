from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("", views.categories, name="categories"),
    path("<str:input_item_type>", views.categories_listings, name="categories_listings")
]