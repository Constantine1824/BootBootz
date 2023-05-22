from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound,ParseError,NotAuthenticated
from .permissions import IsVerified
from .models import Boots
from .serializers import AddressCreationSerializer,BootsSerializer,ReviewsSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

class ProductsListApiView(ListAPIView):
    serializer_class =BootsSerializer
    queryset = Boots.objects.all()
    filter_backends = [OrderingFilter]
    pagination_class = PageNumberPagination

class ProductsRetrieveApiView(APIView):
    def get(self,request,slug):
        boot = Boots.objects.get(slug=slug)
        serializer = BootsSerializer(boot)
        return Response(serializer.data)

class NewArrivalsApiView(ListAPIView):
    """This view should return a queryset based on how long the goods has been added
    that is it should return a queryset of products added within the range of 5days.
    """
    serializer_class = BootsSerializer
    queryset = Boots.objects.filter(newly_added= True)

class SearchApiView(APIView):
    def get(self,request):
        query = request.GET.get('q')
        if query is not None:
            products_query = Boots.objects.filter(
                Q(name__icontains=query)|
                Q(category__icontains=query)|
                Q(manufacturer__icontains=query)
            )
            if products_query:
                serializer = BootsSerializer(products_query,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                raise NotFound()
        else:
            raise ParseError()
    
class CategoryAPIView(APIView):
    def get(self,request,pk):
        boot_obj = Boots.objects.filter(category=pk)
        if boot_obj is not None:
            serializer = BootsSerializer(boot_obj,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        raise NotFound()
    
class ManufacturerAPIView(APIView):
    def get(self,request,pk):
        boot_obj = Boots.objects.filter(manufacturer=pk)
        if boot_obj is not None:
            serializer = BootsSerializer(boot_obj,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
           raise NotFound()

class ReviewsAPIView(APIView):
    """This view handles both the creation of a new review and retrieval of all 
        reviews related to that product
    """
    def post(self,request):
        # Only authenticated users should be able to drop a review
        try:
            if not request.user.is_authenticated and request.user.is_verified:
                raise NotAuthenticated('User must be authenticated to drop a review')
            data = request.data
            serializer = ReviewsSerializer(data=data,user=request.user)
            if serializer.is_valid(raise_exception=True):
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        except AttributeError: # Anonymous users throw an AttributeError
            raise NotAuthenticated('User must be authenticated to drop a review')
        
    def get(self,request):
        # Get all reviews for that particular product
        # Using the product name 
        name = request.GET.get('name')
         # If the product name is not provided, raise an exception
        if name is None:
            raise ParseError('Product name should be provided')
        try:
            boots_obj = Boots.objects.get(name=name)
            reviews = boots_obj.reviews_set.all()
            serializer = ReviewsSerializer(reviews,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Boots.DoesNotExist:
            raise NotFound('Product with the given name does not exist ')
        

class CreateAddressApiView(APIView):
    """This view creates address for an authenticated and verified user"""
    permission_classes = [IsAuthenticated,IsVerified]
    def post(self,request):
        data = request.data
        serializer = AddressCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
# Create your views here.
