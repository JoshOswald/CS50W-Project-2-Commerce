from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import util

from .models import User, Item, ItemDescription

class NewListingForm(forms.Form):
    item_name = forms.CharField(label="Item name:", widget=forms.TextInput(attrs={
        "autofocus":"True", "class":"form-control", "type":"text", "name":"item title", "placeholder":"Title"
    }))
    item_image = forms.URLField(required=False, widget=forms.URLInput(attrs={
        "autofocus":"True", "class":"form-control", "type":"text", "name":"item image", "placeholder":"Link to item image"
    }))
    item_type = forms.ChoiceField(required=False, choices=Item._meta.get_field('item_type').choices, widget=forms.Select(attrs={
        "autofocus":"True", "class":"form-control", "name":"item type", "placeholder":"Item Type"
    }))
    item_description = forms.CharField(widget=forms.Textarea(attrs={
        "autofocus":"True", "class":"form-control", "placeholder":"Item Description", "maxlength":"1000"
        }))
    starting_bid = forms.DecimalField(max_digits=19, decimal_places=2, widget=forms.NumberInput(attrs={
        "autofocus":"True", "class":"form-control", "type":"number", "min":"0", "step":"0.01", "name":"starting bid", "placeholder":"Starting Bid"
    }))

def index(request):
    #Load all listings from DB
    #items = Item.objects.all()
    #items_desc = ItemDescription.objects.all()
    items = Item.objects.select_related('item_owner')
    #Need: Item Name, Description, and 
    return render(request, "auctions/index.html", {
        "items": items
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newListing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            try:
                user = request.user
            except KeyError or User.DoesNotExist:
                return HttpResponseBadRequest("Bad Request: User not Authenticated or does not Exist")
            #Add to db
            item = util.addItem(form, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            item_types = list(dict(Item._meta.get_field('item_type').choices).values())
            return render(request, "auctions/new_listing.html", {
                        "form": form,
                        "item_types": item_types,
                        "message": "There was an error processing your request."}) 
    #If not submitting new listing go here
    else:
        form = NewListingForm()
        #item_types = Item._meta.get_field('item_type').choices
        item_types = list(dict(Item._meta.get_field('item_type').choices).values())
        return render(request, "auctions/new_listing.html", {
            "form": form,
            "item_types": item_types})