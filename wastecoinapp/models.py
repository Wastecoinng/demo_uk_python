from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import datetime

# Create your models here.
class WastecoinUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30,verbose_name="Firstname",blank=True)
    lastname = models.CharField(max_length=30,verbose_name="Lastname",blank=True)
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    user_phone = models.CharField(max_length=15, unique=True, null=True, verbose_name="Telephone number")
    user_gender = models.CharField(max_length=15, verbose_name="Gender")
    user_password = models.TextField(max_length=200,verbose_name="Password")
    user_address = models.TextField(max_length=200,verbose_name="Address")
    user_state = models.TextField(max_length=200,verbose_name="State")
    user_lga = models.TextField(max_length=200,verbose_name="LGA")
    user_country = models.TextField(max_length=200,verbose_name="Country")
    accountname = models.TextField(max_length=200,verbose_name="Account Name", blank=True)
    accountnumber = models.CharField(max_length=10,  null=True, verbose_name="Account Number", blank=True)
    bank = models.TextField(max_length=200,verbose_name="Bank", blank=True)
    currentUserWastecoinBalance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Current WasteCoin Balance", default=0.00)
    date_added = models.DateTimeField(default=timezone.now)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.user} - {self.firstname} - {self.lastname} - {self.email} - {self.user_phone} - {self.user_gender} - {self.user_address}- {self.user_state} - {self.user_lga} - {self.user_country} - {self.date_added} - {self.accountname} - {self.accountnumber} - {self.bank} - {self.currentUserWastecoinBalance}- {self.date_added_normal}"

class WastecoinAgent(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30,verbose_name="Firstname",blank=True)
    lastname = models.CharField(max_length=30,verbose_name="Lastname",blank=True)
    email = models.EmailField(max_length=90, unique=True,verbose_name="Email")
    user_phone = models.CharField(max_length=15, unique=True, null=True, verbose_name="Telephone number")
    user_gender = models.CharField(max_length=15, verbose_name="Gender")
    user_password = models.TextField(max_length=200,verbose_name="Password")
    user_address = models.TextField(max_length=200,verbose_name="Address")
    user_state = models.TextField(max_length=200,verbose_name="State")
    user_lga = models.TextField(max_length=200,verbose_name="LGA")
    user_country = models.TextField(max_length=200,verbose_name="Country")
    accountname = models.TextField(max_length=200,verbose_name="Account Name", blank=True)
    accountnumber = models.CharField(max_length=10,  null=True, verbose_name="Account Number", blank=True)
    bank = models.TextField(max_length=200,verbose_name="Bank", blank=True)
    currentAgentWastecoinBalance = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Current WasteCoin Balance", default=5000.00)
    date_added = models.DateTimeField(default=timezone.now)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.user} - {self.firstname} - {self.lastname} - {self.email} - {self.user_phone} - {self.user_gender} - {self.user_address}- {self.user_state} - {self.user_lga} - {self.user_country} - {self.date_added} - {self.accountname} - {self.accountnumber} - {self.bank} - {self.currentAgentWastecoinBalance}- {self.date_added_normal} "



class Coin(models.Model):
    date_added = models.DateTimeField(default=timezone.now)
    date_added_normal = models.DateField(default=datetime.date.today)
    state = models.TextField(max_length=200,verbose_name="State", default="Lagos")
    month = models.TextField(max_length=200,verbose_name="Month", default="June")
    year = models.CharField(max_length=200,verbose_name="Year", default="2020")
    allocatedCoins = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Allocated Coins", default=70000.00)
    backAllocatedCoins = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Back Allocated Coins", default=0.00)
    exchangeRate = models.DecimalField(max_digits=5,decimal_places=2, verbose_name="Exchange Rate", default=9.99)

    def __str__(self):
        return f"{self.date_added} - {self.state} - {self.month} - {self.year} - {self.allocatedCoins} - {self.backAllocatedCoins}- {self.exchangeRate}- {self.date_added_normal}"

class otp(models.Model):
    user=models.CharField(max_length=200,verbose_name="User")
    # user_phone = models.CharField(max_length=200, unique=True, null=True, verbose_name="Telephone number")
    otp_code = models.IntegerField(verbose_name="OTP",blank=False)
    validated = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    otp_reset_code = models.IntegerField(verbose_name="Reset Code",default="0000")

    def __str__(self):
        return f"{self.user} - {self.otp_code} - {self.validated} - {self.date_added} - {self.otp_reset_code}"


class Transaction(models.Model):
    sender=models.CharField(max_length=30,verbose_name="Sender")
    recipient=models.CharField(max_length=30,verbose_name="Recipient")
    transaction_type=models.CharField(max_length=30,verbose_name="Transaction type", default="NA")
    # amount = models.CharField(max_length=30,verbose_name="Amount of WasteCoin",default="0")
    amount = models.DecimalField(decimal_places=2, max_digits=20,verbose_name="Amount of WasteCoin",default=0.00)
    date_added = models.DateTimeField(default=timezone.now)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.sender} - {self.recipient} - {self.amount}- {self.date_added} - {self.date_added_normal}"

class minedCoin(models.Model):
    miner=models.CharField(max_length=30,verbose_name="Miner")
    creditedBy=models.CharField(max_length=30,verbose_name="Credit by Agent")
    minedCoin = models.DecimalField(decimal_places=2, max_digits=20,verbose_name="Mined Coin",default=0.00)
    date_added = models.DateTimeField(default=timezone.now)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.miner} - {self.creditedBy} - {self.minedCoin} - {self.date_added}- {self.date_added_normal}"

class redeemCoin(models.Model):
    miner=models.CharField(max_length=30,verbose_name="Miner")
    incentive=models.CharField(max_length=30,verbose_name="Incentive")
    redeemedCoin = models.DecimalField(decimal_places=2, max_digits=20,verbose_name="Redeemed Coin",default=0.00)
    date_added = models.DateTimeField(default=timezone.now)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.miner} - {self.incentive} - {self.redeemedCoin} - {self.date_added}- {self.date_added_normal}"

class notifications(models.Model):
    sender=models.CharField(max_length=30,verbose_name="Sender", default="Admin")
    header=models.TextField(max_length=2000,verbose_name="Header", default="headings")
    message=models.TextField(max_length=2000,verbose_name="Message")
    receiver = models.CharField(max_length=30,verbose_name="Reciever",default="0")
    beenRead = models.TextField(max_length=20,verbose_name="Read Message", default="No")
    date_added = models.DateTimeField(default=timezone.now)
    date_added_normal = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.sender} -{self.header} - {self.message} - {self.receiver} - {self.date_added}- {self.date_added_normal}"

# class logs(models.Model):
#     log_message=models.TextField(max_length=2000,verbose_name="log_message")
#     date_added = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.log_message} -{self.date_added}"