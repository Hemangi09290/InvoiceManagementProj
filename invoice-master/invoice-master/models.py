from django.db import models
from django.core.validators import RegexValidator
from tinymce.models import HTMLField
from GameModule.models import *
from user_profile.models import *
from django.contrib.auth.models import User
from django_random_id_model import RandomIDModel


class PlayersDetails(RandomIDModel):

    # Phone No Validation
    # phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    # Phone No Validation

    addedBy = models.ForeignKey(UsersProfile, on_delete=models.PROTECT, default=1)
    player_name = models.CharField(max_length=256, null=False, blank=False, default="Sweepstakes Games Vendor")
    players_phone = models.CharField(max_length=20, null=True, blank=True)
    players_email = models.EmailField(null=True, blank=True, default="info@sweepstakesnearme.com")
    players_cashtag = models.CharField(max_length=20, null=True, blank=True, default="$zudamoon")
    players_facebook_profile = models.URLField(default="https://www.facebook.com", null=True, blank=True)
    about_player = HTMLField(null=True, blank=True, default="No Descriptions")
    player_age = models.IntegerField(null=True, blank=True, default=18)
    player_state = models.CharField(max_length=10, null=True, blank=True, default="LA")
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.player_name


class GameAccountsForPlayers(models.Model):

    games = models.ForeignKey(Games, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user_name = models.CharField(max_length=20, null=False, blank=False, default="username")
    user_pswd = models.CharField(max_length=20, null=False, blank=False, default="password")
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.user_name


class AssignAccountToPlayer(models.Model):
    gameaccountsforplayers = models.ForeignKey(GameAccountsForPlayers, on_delete=models.PROTECT)
    playersdetails = models.ForeignKey(PlayersDetails, on_delete=models.PROTECT, default=1)
    assigned_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    def __str__(self):
        return str(self.gameaccountsforplayers)


class PlayerAccountRecharge(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    gameaccountsforplayers = models.ForeignKey(GameAccountsForPlayers, on_delete=models.PROTECT)
    playersdetails = models.ForeignKey(PlayersDetails, on_delete=models.PROTECT, default=1)
    rechargetype = models.ForeignKey(RechargeType, on_delete=models.PROTECT, default=1)
    recharge_amount = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False, default=00)
    recharge_credit = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False, default=00)
    recharge_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    def __str__(self):
        return str(self.gameaccountsforplayers)


class PlayerAccountCashout(models.Model):
    playeraccountrecharge = models.ForeignKey(PlayerAccountRecharge, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    paymentmethod = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    cashout_amount = models.IntegerField(null=False, blank=False, default=00)
    redeemed_points = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, default=00)
    deposit_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    cashout_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    updated_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    def __str__(self):
        return str(self.playeraccountrecharge__method_identity)