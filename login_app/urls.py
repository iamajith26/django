from django.urls import path, include
from . import views
from .views import ProtectedView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected', ProtectedView.as_view(), name='protected'),
]
