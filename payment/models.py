from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models


class Transaction(models.Model):

    class StatusChoices(models.TextChoices):
        created = "CREATED", _("Created")
        succeeded = "SUCCEEDED", _("Succeeded")
        canceled = "CANCELED", _("Canceled")

    class TagChoices(models.IntegerChoices):
        refill = 0, _("Refill")
        subscription = 1, _("Subscription")
        premium = 2, _("Premium")

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    octo_payment_uuid = models.CharField(unique=True, max_length=128, null=True, blank=True)
    status = models.CharField(max_length=32, choices=StatusChoices.choices, default="CREATED")
    payment_method = models.CharField(max_length=128)
    tag = models.IntegerField(choices=TagChoices.choices)

    total_sum = models.DecimalField(max_digits=12, decimal_places=2)
    transfer_sum = models.DecimalField(max_digits=12, decimal_places=2, null=True,blank=True)

    additional_data = models.JSONField(blank=True, default=dict)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
