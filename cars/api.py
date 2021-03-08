from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from cars.models import Car, BrandName, ModelName, CarImage
from rest_framework import viewsets, permissions, mixins, generics, status
from .serializers import CarSerializer, BrandnameSerializer, ModelnameSerializer, CarImageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from cars.permissions import PostOwnCar
from .service import PaginationCars, CarFilter, BrandModelFilter


class BrandnameViewSet(viewsets.ModelViewSet):
    queryset = BrandName.objects.all()
    serializer_class = BrandnameSerializer


class ModelnameViewSet(viewsets.ModelViewSet):
    queryset = ModelName.objects.all()
    serializer_class = ModelnameSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BrandModelFilter


# class CarViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#
#     def perform_create(self, serializer):
#         author = get_object_or_404(Author, id=self.request.data.get('author_id'))
#         return serializer.save(author=author)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, *kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class CarViewSet(viewsets.ModelViewSet):
#     # def get_queryset(self):
#     #     return Car.objects.filter(id=self.request.data.get('car_id'))
#
#     # lookup_field = 'car_id'
#     serializer_class = CarSerializer
#     queryset = Car.objects.all()

# def retrieve(self, request, *args, **kwargs): # Change is here <<
#     serializer = self.get_serializer(self.get_queryset(), many=True)
#     return Response(data=serializer.data)

class CarImageViewSet(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    # parser_classes = (MultiPartParser, FormParser,)

    # def perform_create(self, serializer):
    #     serializer.save(image=self.request.data.get('image'))

class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    pagination_class = PaginationCars
    filter_backends = (DjangoFilterBackend,)
    filter_class = CarFilter
    permission_classes = (PostOwnCar, permissions.IsAuthenticatedOrReadOnly)
    # parser_classes = (MultiPartParser, FormParser,)


    # def post(self, request, format=None):
    #     serializer = CarSerializer(data=request.DATA)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ordering = ('brand_name',)
    # # filter_fields = ('brand_name', 'body_type', 'fuel_type')
    # permission_classes = [
    #     permissions.AllowAny
    # ]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #
    # def get_queryset(self):
    #     return Car.objects.filter(moderate_on=True)
# queryset = Car.objects.all()

# def get_queryset(self):

# return self.request.user.cars.all()
# return self.queryset.filter(owner=self.request.user)

# def perform_create(self, serializer):
# 	serializer.save(owner=self.request.user)
