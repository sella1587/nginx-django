from django.urls import path
from .views import GetObjectConsolidated, ConsolidatedDataView, ImportJsonView
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('getDataConsolided/', GetObjectConsolidated.as_view(), name='getDataConsolided'),
    path('Getinfobrute/', ConsolidatedDataView.as_view(), name='getrawdata'),
    path('LoadJsonData/', ImportJsonView.as_view(), name='loadjsondata'),
]