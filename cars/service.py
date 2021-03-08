from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
from .models import Car, ModelName


class PaginationCars(PageNumberPagination):
    page_size = 3
    max_page_size = 1000


class BrandModelFilter(filters.FilterSet):
    name = filters.AllValuesFilter('name')

    class Meta:
        model = ModelName
        fields = ('brandname', 'name')

class CarFilter(filters.FilterSet):
    # brand_name = filters.AllValuesFilter('brand_name')
    # model_name = filters.CharFilter('model_name')
    body_type = filters.CharFilter('body_type')
    fuel_type = filters.CharFilter('fuel_type')
    # mileage = filters.
    car_release_date = filters.RangeFilter()
    price = filters.RangeFilter()

    class Meta:
        model = Car
        fields = ('brand_name', 'model_name', 'body_type', 'fuel_type', 'car_release_date', 'price')
