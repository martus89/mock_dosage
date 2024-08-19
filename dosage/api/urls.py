from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApprovedDrugViewSet, ProductViewSet, StorageViewSet, UserViewSet, DrugFormViewSet

router = DefaultRouter()

router.register(r'approved-drugs', ApprovedDrugViewSet)
router.register(r'products', ProductViewSet)
router.register(r'storages', StorageViewSet)
router.register(r'users', UserViewSet)
router.register(r'drug-form', DrugFormViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
