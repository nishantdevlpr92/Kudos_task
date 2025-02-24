from django.urls import path
from .views import SendKudosView, ReceivedKudosView, CurrentUserView,UsersListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("kudos/", SendKudosView.as_view(), name="give_kudos"),
    path("kudos/received/", ReceivedKudosView.as_view(), name="received_kudos"),
    path("user/current/", CurrentUserView.as_view(), name="current_user"),
    path("users/", UsersListAPIView.as_view(), name="users-in-org")
]
