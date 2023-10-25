from django.contrib import admin

from payment import models


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("pk", "status", "tag", "total_sum", "transfer_sum", "updated_at", "created_at")
