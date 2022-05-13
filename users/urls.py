from django.urls import path
from users.views import KakaoLogInView

urlpatterns = [
    path('/login/kakao', KakaoLogInView.as_view())
]