from django.urls import path

from payment import views


app_name = "payment"

urlpatterns = [
    path("", views.SubscriptionPaymentView.as_view(), name="index"),
    path("notify/", views.NotifyView.as_view(), name="notify"),
    path("success/", views.SuccessView.as_view(), name="success"),
]
