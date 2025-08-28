from django.urls import path,include
from .views import BookViewSet, BorrowViewSet, RegisterView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrows', BorrowViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(),name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name  = 'token_refresh'),
    path('api/register/', RegisterView.as_view(), name = "register")
]
