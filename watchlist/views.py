from django.shortcuts import render
from django.db import models

from auctions.models import User, Item, WatchList

# Create your views here.
def watchlist(request):

    if request.user.is_authenticated:
        user = request.user
        watchListItems = WatchList.objects.filter(user=user).values_list("item", flat=True)
        items = Item.objects.filter(id__in=watchListItems)
        return render(request, "watchlist/watchlist.html", {
            "items": items
        })

    else:
        items = Item.objects.select_related('item_owner')
        #Need: Item Name, Description, and 
        return render(request, "auctions/index.html", {
            "items": items,
            "error": "You Must Be Logged In For This Action."
        })