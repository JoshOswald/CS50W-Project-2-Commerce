from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from django.contrib.auth.models import User
from auctions.models import Item, ItemDescription

# Create your views here.
def listing(request, item_id):
    try:
        items = Item.objects.select_related('item_owner')
        item = items.get(id=item_id)
    except Item.DoesNotExist:
        raise Http404("Item Listing Not Found.")
    return render(request, "listings/listing.html", {
        "item": item,
        "item_name": item.item_name
    })