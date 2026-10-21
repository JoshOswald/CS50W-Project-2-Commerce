from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from django.contrib.auth.models import User
from auctions.models import Item, ItemDescription, ItemBid, UserComment, WatchList

from auctions import util

class NewCommentForm(forms.Form):
    user_comment = forms.CharField(widget=forms.Textarea(attrs={
            "class":"form-control comment-box", "placeholder":"Comment", "maxlength":"500"
        }))

class NewBidForm(forms.Form):
    bid = forms.DecimalField(max_digits=19, decimal_places=2, widget=forms.NumberInput(attrs={
            "class":"form-control", "min":"0", "placeholder":"Enter Bid"
        }))

class WishlistForm(forms.Form):
    wishList = forms.BooleanField(label="Add To Wishlist:", widget=forms.CheckboxInput(attrs={'onchange': 'this.form.submit();'}))

class closeListing(forms.Form):
    closeListing = forms.BooleanField(label="Close Listing")

# Create your views here.
def listing(request, item_id):

    #Invalid Item Request
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return render(request, "listings/listing.html", {
                "error": "Hm, we do not have the item you are looking for."
            })

    #DO NOT CHANGE ITEM OR FORMS!
    forms = util.getListingForms()
    itemOwnerForms = [NewCommentForm(), closeListing()]
    #item = Item.objects.get(id=item_id)
    #comments = UserComment.objects.get(item=item_id)
    comments = UserComment.objects.filter(item=item.id)
    bids = ItemBid.objects.filter(item=item.id)
    try:
        max_bid = bids.order_by('-bid')[0]
    except:
        max_bid = None
    wishListed = False

    #Check is user is logged in
    if request.user.is_authenticated:
        user = request.user

        #Check is user already watch listed item
        try:
            wishListed = WatchList.objects.get(user=user, item=item.id)
            #forms[2] = WishlistForm(initial={'wishList': True})
        except WatchList.DoesNotExist:
            wishListed = None

        if request.method == "POST":
            #ITEM OWNER STUFF
            if item.item_owner.id == user.id:
                forms = itemOwnerForms
                if "closeListing" in request.POST:
                    form = closeListing(request.POST)
                    if form.is_valid():
                        item.item_sold = True
                        item.save()
                        return render(request, "listings/listing.html", {
                                "item": item,
                                "bids": len(bids),
                                "max_bid": max_bid,
                                "forms": forms,
                                "commentForm": NewCommentForm(),
                                "comments": comments,
                                "message": "Listing Has Ended Successfully."
                            })
                    else:
                        if item.item_sold:
                            closeListingBool = None
                        else:
                            closeListingBool = closeListing()
                        return render(request, "listings/listing.html", {
                                "item": item,
                                "bids": len(bids),
                                "max_bid": max_bid,
                                "forms": forms,
                                "commentForm": NewCommentForm(),
                                "closeListing": closeListingBool,
                                "comments": comments,
                                "error": "There Was An Error Processing Your Request."
                            })

                #New comment post request
                if "user_comment" in request.POST:
                    form = NewCommentForm(request.POST)
                    if item.item_sold:
                        closeListingBool = None
                    else:
                        closeListingBool = closeListing()
                    if form.is_valid():
                        UserComment.objects.create(user=user, item=item.id, comment=form.cleaned_data["user_comment"])
                    return render(request, "listings/listing.html", {
                            "item": item,
                            "bids": len(bids),
                            "max_bid": max_bid,
                            "forms": forms,
                            "commentForm": NewCommentForm(),
                            "closeListing": closeListingBool,
                            "comments": comments
                            
                        })
            #ITEM OWNER STUFF ^^

            #NOT OWNER OF ITEM
            else:
                #New comment post request
                if "user_comment" in request.POST:
                    form = NewCommentForm(request.POST)
                    print(item)
                    if form.is_valid():
                        UserComment.objects.create(user=user, item=item.id, comment=form.cleaned_data["user_comment"])
                    else:
                        return render(request, "listings/listing.html", {
                                "item": item,
                                "bids": len(bids),
                                "max_bid": max_bid,
                                "forms": forms,
                                "comments": comments,
                                "wishListed": wishListed,
                                "commentForm": NewCommentForm(),
                                "bidForm": NewBidForm(),
                                "wishListForm": WishlistForm(),
                                "error": "There Was An Error Processing Your Request."
                            })
                    return render(request, "listings/listing.html", {
                            "item": item,
                            "bids": len(bids),
                            "max_bid": max_bid,
                            "forms": forms,
                            "comments": comments,
                            "wishListed": wishListed,
                            "commentForm": NewCommentForm(),
                            "bidForm": NewBidForm(),
                            "wishListForm": WishlistForm()
                        })
                if "bid" in request.POST:
                    return bid(request, item, max_bid, bids)
                if "wishList" in request.POST:
                    if wishListed is not None:
                        wishListed.delete()
                        wishListed = None
                        message = "Item Has Been Removed From Wishlist."
                    else:
                        wishListed = WatchList.objects.create(user=user, item=item.id)
                        message = "Item Has Been Added To Wishlist."
                    return render(request, "listings/listing.html", {
                            "item": item,
                            "bids": len(bids),
                            "max_bid": max_bid,
                            "forms": forms,
                            "comments": comments,
                            "wishListed": wishListed,
                            "message": message,
                            "commentForm": NewCommentForm(),
                            "bidForm": NewBidForm(),
                            "wishListForm": WishlistForm()
                        })
                else:
                    #If get request but no match
                    return render(request, "listings/listing.html", {
                            "item": item,
                            "bids": len(bids),
                            "max_bid": max_bid,
                            "forms": forms,
                            "comments": comments,
                            "wishListed": wishListed,
                            "commentForm": NewCommentForm(),
                            "bidForm": NewBidForm(),
                            "wishListForm": WishlistForm()
                        })


        #User is logged in AND request is not POST
        else:
            #If owner
            if item.item_owner.id == user.id:
                forms = itemOwnerForms
                if item.item_sold:
                    closeListingBool = None
                else:
                    closeListingBool = closeListing()
                return render(request, "listings/listing.html", {
                        "item": item,
                        "bids": len(bids),
                        "max_bid": max_bid,
                        "forms": forms,
                        "comments": comments,
                        "wishListed": wishListed,
                        "commentForm": NewCommentForm(),
                        "closeListing": closeListingBool
                    })
            else:
                return render(request, "listings/listing.html", {
                        "item": item,
                        "bids": len(bids),
                        "max_bid": max_bid,
                        "forms": forms,
                        "comments": comments,
                        "wishListed": wishListed,
                        "commentForm": NewCommentForm(),
                        "bidForm": NewBidForm(),
                        "wishListForm": WishlistForm()
                    })
    #User is not logged in
    else:
        if request.method == "POST":
            if request.POST:
                return render(request, "listings/listing.html", {
                        "item": item,
                        "bids": len(bids),
                        "max_bid": max_bid,
                        "comments": comments,
                        "error": "You Must Be Logged In For This Action!"
                    })
        #User is not logged in AND request is not POST
        else:
            return render(request, "listings/listing.html", {
                    "item": item,
                    "bids": len(bids),
                    "max_bid": max_bid,
                    "comments": comments
                })

def bid(request, item, max_bid, bids):
    user = request.user
    forms = util.getListingForms()
    comments = UserComment.objects.filter(item=item.id)
    #If listing is over
    if item.item_sold:
        return render(request, "listings/listing.html", {
                "item": item,
                "bids": len(bids),
                "max_bid": max_bid,
                "forms": forms,
                "comments": comments,
                "error": "Listing Has Been Ended.",
                "wishListForm": WishlistForm()
        })

    form = NewBidForm(request.POST)

    if form.is_valid():
        bid_amount = form.cleaned_data["bid"]

        #Start Bidding
        if item.item_current_bid == None:
            if bid_amount == item.item_starting_bid or bid_amount > item.item_starting_bid:
                ItemBid.objects.create(item=item.id,user=user,bid=form.cleaned_data["bid"])
                return render(request, "listings/listing.html", {
                        "item": item,
                        "bids": len(bids),
                        "max_bid": max_bid,
                        "forms": forms,
                        "comments": comments,
                        "message": "Bid Entered Successfully!",
                        "commentForm": NewCommentForm(),
                        "bidForm": NewBidForm(),
                        "wishListForm": WishlistForm()
                    })
            else:
                return render(request, "listings/listing.html", {
                        "item": item,
                        "bids": len(bids),
                        "max_bid": max_bid,
                        "forms": forms,
                        "comments": comments,
                        "error": "Bid Must Be Greater Or Equal To Starting Bid.",
                        "commentForm": NewCommentForm(),
                        "bidForm": NewBidForm(),
                        "wishListForm": WishlistForm()
                    })
                
        #If bid is too low
        if bid_amount == item.item_current_bid or bid_amount < item.item_current_bid:
            return render(request, "listings/listing.html", {
                    "item": item,
                    "bids": len(bids),
                    "max_bid": max_bid,
                    "forms": forms,
                    "comments": comments,
                    "error": "Bid Is Lower Or Equal To Current Highest Bid!",
                    "commentForm": NewCommentForm(),
                    "bidForm": NewBidForm(),
                    "wishListForm": WishlistForm()
                })
        #If bid is higher
        else:
            ItemBid.objects.create(item=item.id,user=user,bid=form.cleaned_data["bid"])
            item.save()
            return render(request, "listings/listing.html", {
                    "item": item,
                    "bids": len(bids),
                    "max_bid": max_bid,
                    "forms": forms,
                    "comments": comments,
                    "message": "Bid Entered Successfully!",
                    "commentForm": NewCommentForm(),
                    "bidForm": NewBidForm(),
                    "wishListForm": WishlistForm()
                })
    else:
        return render(request, "listings/listing.html", {
                        "item": item,
                        "bids": len(bids),
                        "max_bid": max_bid,
                        "forms": forms,
                        "comments": comments,
                        "error": "There Seems To Be A Problem With Your Bid Request.",
                        "commentForm": NewCommentForm(),
                        "bidForm": NewBidForm(),
                        "wishListForm": WishlistForm()
                })