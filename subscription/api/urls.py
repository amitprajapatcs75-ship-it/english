from django.urls import path
from . import views


urlpatterns = [
    path("plan/", views.SubscriptionPlanApiView.as_view(), name="users_plan"),
]