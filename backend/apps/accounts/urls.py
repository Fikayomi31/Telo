from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import TailorLoginView, TailorRegistrationView, TailorProfileView


urlpatterns = [

    path("register/", TailorRegistrationView.as_view(), name="tailor-register"),
    path("login/", TailorLoginView.as_view(), name="tailor-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", TailorProfileView.as_view(), name="tailor-profile"),
]