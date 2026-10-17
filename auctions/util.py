from .models import User, Item, ItemDescription, UserComment

from listings.views import NewCommentForm, NewBidForm, WishlistForm

def addItem(form, user):
    item = Item.objects.create(
        item_owner=user,
        item_name=form["item_name"],
        item_image_link=form["item_image"],
        item_type=form["item_type"],
        item_starting_bid=form["starting_bid"],
        item_current_bid=form["starting_bid"])
    des = ItemDescription.objects.create(
        item=item,
        item_description=form["item_description"]
    )
    return item

def addComment(form, user, item_id):
    comment = UserComment.objects.create(
        item=item_id,
        user=user,
        comment=form["user_comment"])
    return comment

def getListingForms():
    forms = [NewCommentForm(), NewBidForm(), WishlistForm()]
    return forms