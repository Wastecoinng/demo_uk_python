from django.contrib import admin
from .models import WastecoinUser,WastecoinAgent,Coin,minedCoin,redeemCoin,notifications,Transaction,otp

# Register your models here.
admin.site.register(WastecoinUser)
admin.site.register(WastecoinAgent)
admin.site.register(Coin)
admin.site.register(minedCoin)
admin.site.register(redeemCoin)
admin.site.register(notifications)
admin.site.register(Transaction)
admin.site.register(otp)
