from rest_framework.viewsets import ModelViewSet
from Core.models import Boots
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serializers import BootsCreationSerializer
from Order.serializers import OrderSerializer
from Order.models import Order
from rest_framework.response import Response
from rest_framework import mixins
from .filters import DateTimeCustomFilter
from rest_framework.filters import SearchFilter,OrderingFilter

class ProductViewSets(ModelViewSet):
    queryset = Boots
    permission_classes = [IsAdminUser,IsAuthenticated]
    serializer_class = BootsCreationSerializer
    filter_backends = [SearchFilter,OrderingFilter,DateTimeCustomFilter]
    lookup_field = 'slug'
    

class OrderViewSets(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet
                    ):
    queryset = Order
    permission_classes = [IsAdminUser,IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter,OrderingFilter,DateTimeCustomFilter]
    lookup_field = 'tracking_id'
    lookup_url_kwarg = 'pk'


# Create your views here.
