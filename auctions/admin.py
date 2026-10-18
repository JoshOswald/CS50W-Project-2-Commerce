from django.contrib import admin

from .models import User, Item, WatchList, ItemDescription, ItemBid, UserComment

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(WatchList)
admin.site.register(ItemDescription)
admin.site.register(ItemBid)
admin.site.register(UserComment)