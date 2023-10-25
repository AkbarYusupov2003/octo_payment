import json
import requests
from decimal import Decimal
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, HttpResponse, get_object_or_404

from payment import models


class SubscriptionPaymentView(View):

    def get(self, request, *args, **kwargs):
        ''' url http://localhost:8000/?username=+998333454115&subscription=1&amount=20000&commission=2.7&payment_method=uzcard_humo'''
        try:
            username = request.GET.get("username")
            tag = int(request.GET.get("subscription"))
            amount = int(request.GET.get("amount"))
            commission = Decimal(request.GET.get("commission"))
            payment_method = request.GET.get("payment_method")
        except:
            return HttpResponse("Wrong data types")

        if not(username and amount and commission):
            return HttpResponse("Not enough params")

        query_to_check_if_subscription_exists = [0, 1, 2, 3]
        available_methods = ["bank_card", "uzcard_humo"]
        if not(tag in query_to_check_if_subscription_exists and 0 < amount and 0 < commission and payment_method in available_methods):
            return HttpResponse("Wrong data values")

        owner = get_object_or_404(get_user_model(), username=username)
        total_sum = amount + amount / Decimal(100) * commission

        try:
            transaction = models.Transaction.objects.get(
                owner=owner,
                octo_payment_uuid__isnull=False,
                status="CREATED",
                payment_method=payment_method,
                tag=tag,
                total_sum=total_sum,
                created_at__gte=timezone.make_aware(
                    datetime.now(), timezone.get_current_timezone()
                ) - timedelta(minutes=1)
            )
            print("Transaction exists, redirecting")
            return redirect(f"https://pay2.octo.uz/pay/{transaction.octo_payment_uuid}")
        except:
            transaction = models.Transaction.objects.create(
                owner=owner,
                tag=tag,
                payment_method=payment_method,
                total_sum=total_sum,
            )

        url = "https://secure.octo.uz/prepare_payment"
        notify_url = "https://8eef-84-54-76-160.ngrok-free.app/notify/"
        return_url = "http://127.0.0.1:8000/success/"

        data = {
            "octo_shop_id": settings.OCTO_SHOP_ID,
            "octo_secret": settings.OCTO_SECRET_KEY,
            "shop_transaction_id": f"{transaction.pk}   ",
            "auto_capture": False,
            "test": True,
            "init_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # "user_data": {
            #   "user_id": transaction.owner.pk,
            #   # "phone": "998971234567",
            #   #"email": transaction.owner.email
            # },
            "total_sum": str(total_sum),
            "currency": "UZS",
            "description": "Оплата платформы Splay.uz",
            "tag": tag,
            "notify_url": notify_url,
            "return_url": return_url
        }

        if payment_method == "bank_card":
            data["payment_methods"] = [{"method": "bank_card"}]

        elif payment_method == "uzcard_humo":
            data["payment_methods"] = [{"method": "uzcard"}, {"method": "humo"}]

        response = requests.post(url, headers={"Content-Type": "application/json"}, json=data).json()
        print("Before payment: ", response)

        if response.get("status") == "created" and response.get("octo_pay_url") and response.get("octo_payment_UUID"):
            transaction.octo_payment_uuid = response.get("octo_payment_UUID")
            transaction.additional_data = {"card_country": response.get("card_country"), "maskedPan": response.get("maskedPan")}
            transaction.save()
            return redirect(response.get("octo_pay_url"))

        return HttpResponse("Unexpected error accused")


class NotifyView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        print("Notify body: ", body)
        pk = body.get("shop_transaction_id")
        octo_payment_uuid = body.get("octo_payment_UUID")
        status = body.get("status")
        total_sum = body.get("total_sum")
        transfer_sum = body.get("transfer_sum")

        if status == "waiting_for_capture":
            try:
                transaction = models.Transaction.objects.get(
                    pk=pk,
                    octo_payment_uuid=octo_payment_uuid,
                    total_sum=total_sum,
                )
                if transaction:

                    query_to_check_if_subscription_exists = [0, 1,2,3]
                    if not(transaction.tag in query_to_check_if_subscription_exists):
                        return HttpResponse("Subscription doesn't exists")

                    url = "https://secure.octo.uz/set_accept"
                    data = {
                        "octo_shop_id": settings.OCTO_SHOP_ID,
                        "octo_secret": settings.OCTO_SECRET_KEY,
                        "octo_payment_UUID": octo_payment_uuid,
                        "accept_status": "capture",
                        "final_amount": transfer_sum
                    }
                    response = requests.post(url, headers={"Content-Type": "application/json"}, json=data).json()
                    print("Notify, response from OCTO: ", response)

                    if response.get("error") == 0 and response.get("status") == "succeeded":
                        transaction.transfer_sum = transfer_sum
                        transaction.status = "SUCCEEDED"
                        transaction.additional_data["signature"] = body.get("signature")
                        transaction.additional_data["hash_key"] = body.get("hash_key")
                        transaction.save()
                        print("\n\n Notify worked")
                        return HttpResponse("")

                    transaction.status = "CANCELED"
                    transaction.save()

            except Exception as e:
                print("Notify exception: ", e)

        print("Notify failed")
        return HttpResponse("")


class SuccessView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse("Success")

