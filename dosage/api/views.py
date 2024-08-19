from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from warehouse.models import Storage, Product, ApprovedDrug, User, DrugFormChoice
from rest_framework import viewsets, mixins
from django_filters import rest_framework as filters
from .serializers import BaseDrugFormChoiceSerializer, ExtendedDrugFormChoiceSerializer, BaseApprovedDrugSerializer, BaseProductSerializer, BaseStorageSerializer, ExtendedStorageSerializer, BaseUserSerializer, ExtendedApprovedDrugSerializer, ExtendedUserSerializer, ExtendedProductSerializer
from .filters import StorageFilter, UserFilter, ProductFilter, ApprovedDrugFilter, DrugFormFilter
from .permissions import IsViewOnly


class DrugFormViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = DrugFormChoice.objects.all()
    serializer_class = BaseDrugFormChoiceSerializer
    permission_classes = [IsAuthenticated, IsViewOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DrugFormFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return BaseDrugFormChoiceSerializer
        elif self.action in ['retrieve', 'create', 'update']:
            return ExtendedDrugFormChoiceSerializer
        return BaseDrugFormChoiceSerializer


class StorageViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Storage.objects.all()
    serializer_class = BaseStorageSerializer
    permission_classes = [IsAuthenticated, IsViewOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StorageFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return BaseStorageSerializer
        elif self.action in ['retrieve', 'create', 'update']:
            return ExtendedStorageSerializer
        return BaseStorageSerializer


    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         queryset = Storage.objects.all().select_related('created_by')
            # print('jestem adminem')
        # else:
            # queryset = Storage.objects.filter(created_by=self.request.user)
            # print('nie jestem adminem')
        # print(queryset)
        # return queryset

    @action(detail=False, methods=['GET'], url_path='total-new-rack-count')
    def total_new_rack_count(self, request):
        total_nr = Storage.objects.filter(rack="NEW").count()
        return Response(total_nr, status=200)


class ApprovedDrugViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                          mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ApprovedDrug.objects.all()
    serializer_class = BaseApprovedDrugSerializer
    permission_classes = [IsAuthenticated, IsViewOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ApprovedDrugFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return BaseApprovedDrugSerializer
        elif self.action in ['retrieve', 'create', 'update']:
            return ExtendedApprovedDrugSerializer
        return BaseApprovedDrugSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='view_only').exists():
            queryset = ApprovedDrug.objects.filter(is_controlled=False)
            return queryset
        return super().get_queryset()


class ProductViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = BaseProductSerializer
    permission_classes = [IsAuthenticated, IsViewOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return BaseProductSerializer
        elif self.action in ['retrieve', 'create', 'update']:
            return ExtendedProductSerializer
        return BaseProductSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.groups.filter(name='view_only').exists():
            queryset = queryset.filter(approved_drug__is_controlled=False)
        return queryset


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = [IsAuthenticated, IsViewOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action in ['list']:
            return BaseUserSerializer
        elif self.action in ['retrieve', 'create', 'update']:
            return ExtendedUserSerializer
        return BaseUserSerializer
