from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from django.contrib.auth.models import User
from auctions.models import Item, ItemDescription

def categories(request):
    try:
        item_types = Item.item_type.field.choices
    except Item.DoesNotExist:
        raise Http404("Could Not Fetch Categories.")
    return render(request, "categories/categories.html", {
        "item_types": item_types
    })

def categories_listings(request, input_item_type):

    valid_types = [value for value, label in Item.item_type.field.choices]

    if input_item_type in valid_types:

        label = dict(Item._meta.get_field("item_type").choices).get(input_item_type)

        if Item.objects.filter(item_type=input_item_type).exists():

            items = Item.objects.filter(item_type=input_item_type)
            return render(request, "categories/categories_listings.html", {
                    "items": items,
                    "input_item_type": label
                })
        else:

            #No listings for specific category
            return render(request, "categories/categories_listings.html", {
                "input_item_type": label
            })
    else:

        #GET request had invalid category
        return render(request, "categories/categories_listings.html", {
            "message": "Category Specified Is Not In System."
        })