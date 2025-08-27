from django.urls import path,include
from .views import BookViewSet, BorrowViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrows', BorrowViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
