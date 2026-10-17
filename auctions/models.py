from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.dateparse import parse_datetime
from django.utils import timezone



class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username} {self.email}"

class Item(models.Model):
    #item_id auto created by django
    item_owner = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE, related_name="owned_item")
    item_name = models.CharField(max_length=64)
    item_image_link = models.CharField(max_length=64)
    item_starting_bid = models.DecimalField(decimal_places=2, max_digits=19)
    item_current_bid = models.DecimalField(decimal_places=2, max_digits=19, null=True)
    item_posted_time = models.DateTimeField(auto_now_add=True)
    item_last_updated = models.DateTimeField(auto_now=True)
    item_sold = models.BooleanField(default=False)

    class item_type(models.TextChoices):
        AllCategories = 'AC', _('All Categories')
        Antiques = 'AN', _('Antiques')
        Art = 'AR', _('Art')
        Baby = 'BA', _('Baby')
        Books = 'BO', _('Books')
        BusinessIndustrial = 'BI', _('Business & Industrial')
        CamerasPhoto = 'CP', _('Cameras & Photo')
        CellPhonesAccessories = 'CA', _('Cell Phones & Accessories')
        ClothingShoesAccessories = 'CS', _('Clothing, Shoes & Accessories')
        CoinsPaperMoney = 'CO', _('Coins & Paper Money')
        Collectibles = 'CL', _('Collectibles')
        ComputersTabletsNetworking = 'CT', _('Computers/Tablets & Networking')
        ConsumerElectronics = 'CE', _('Consumer Electronics')
        Crafts = 'CR', _('Crafts')
        DollsBears = 'DB', _('Dolls & Bears')
        DVDsMovies = 'DM', _('DVDs & Movies')
        EntertainmentMemorabilia = 'EM', _('Entertainment Memorabilia')
        EverythingElse = 'EE', _('Everything Else')
        GiftCards = 'GC', _('Gift Cards')
        HealthBeauty = 'HB', _('Health & Beauty')
        HomeGarden = 'HG', _('Home & Garden')
        JewelryWatches = 'JW', _('Jewelry & Watches')
        Music = 'MU', _('Music')
        MusicalInstrumentsGear = 'MI', _('Musical Instruments & Gear')
        PetSupplies = 'PS', _('Pet Supplies')
        PotteryGlass = 'PG', _('Pottery & Glass')
        RealEstate = 'RE', _('Real Estate')
        SpecialtyServices = 'SS', _('Specialty Services')
        SportingGoods = 'SG', _('Sporting Goods')
        SportsMemorabilia = 'SM', _('Sports Mem, Cards & Fan Shop')
        Stamps = 'ST', _('Stamps')
        Tickets = 'TI', _('Tickets & Experiences')
        ToysHobbies = 'TH', _('Toys & Hobbies')
        Travel = 'TR', _('Travel')
        VideoGamesConsoles = 'VG', _('Video Games & Consoles')
        
    item_type = models.CharField(
        max_length=2,
        choices=item_type,
        default=item_type.AllCategories
        )

    def __str__(self):
        return f"{self.id} {self.item_name}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item_ref")
    item = models.PositiveIntegerField(Item)

    def __str__(self):
        return f"{self.user.id} {self.item.id}"

class ItemDescription(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    item_description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.item.id} {self.item_description}"

class ItemBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bidding")
    item = models.PositiveIntegerField(Item)
    bid = models.DecimalField(decimal_places=2, max_digits=19)

    def __str__(self):
        return f"User:{self.user.id} Item:{self.item.id} Bid:{self.bid}"

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    item = models.PositiveIntegerField(Item)
    comment = models.CharField(max_length=500)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User:{self.user.id} Item:{self.item.id} Comment:{self.comment}"

class UserWatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.PositiveIntegerField(Item)

    def __str__(self):
        return f"User:{self.user.id} Item:{self.item.id}"