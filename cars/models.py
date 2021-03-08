from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
import re

from accounts.models import CustomUser


class BrandName(models.Model):
    # brand_id = models.IntegerField(primary_key=True)
    brandname = models.CharField(max_length=100)

    # url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.brandname

    # class Meta:
    #     db_table = 'brandname'


class ModelName(models.Model):
    brandname = models.ForeignKey(BrandName, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    # def brand_name(self):
    #     return self.brand.brand_name
    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = 'name'

# r = requests.get('https://turbo.az/')
# soup = BeautifulSoup(r.text, 'html.parser')
# br_list = soup.find('select', {'name': 'q[make][]'}).text.split('\n')
# BRAND_CHOICES = []
# for brand in br_list:
#     BRAND_CHOICES.append((brand, brand))
#
r2 = requests.get('https://az.wikipedia.org/wiki/Az%C9%99rbaycan_%C5%9F%C9%99h%C9%99rl%C9%99ri')
soup2 = BeautifulSoup(r2.text, 'html.parser')
CITY_CHOICES = []

for i in range(1, 81):
    if i == 5:
        continue
    city = soup2.find_all('tr')[i].find_all('td')[0].text
    if '\n' in city:
        city = city.replace("\n", "")
    CITY_CHOICES.append((city, city))


class Car(models.Model):
    # Parsing brand names from turbo az to make dropdown menu for brands
    # brand_name = models.CharField(max_length=100, default='Bütün markalar')
    # model_name = models.CharField(max_length=100, default='Bütün modellər')
    brand_name = models.ForeignKey(BrandName, on_delete=models.SET_NULL, null=True)
    model_name = models.ForeignKey(ModelName, on_delete=models.SET_NULL, null=True)
    BODY_TYPE_CHOICES = (
        ('Sedan', "Sedan"),
        ('Hatchback', "Hatchback"),
        ('SUV', "SUV"),
        ('Coupe', "Coupe"),
        ('Convertible', "Convertible"),
        ('Wagon', "Wagon"),
        ('Van', "Van"),
        ('Minivan', "Jeep"),
        ('Jeep', "Jeep"),
        ('Pickup', "Pickup"),
    )
    body_type = models.CharField(max_length=100,
                                 choices=BODY_TYPE_CHOICES,
                                 default='Sedan')
    # body_type = models.CharField(max_length=100, default='Sedan', blank=True, null=True)
    FUEL_TYPE_CHOICES = (
        ('Petrol', "Petrol"),
        ('Diesel', "Diesel"),
        ('Gas', "Gas"),
        ('Electro', "Electro"),
        ('Hybrid', "Hybrid"),
    )
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPE_CHOICES, default='Petrol')
    mileage = models.IntegerField(default=0)
    COLOUR_CHOICES = [
                       ('Ağ', 'Ağ'),
                       ('Bej', 'Bej'),
                       ('Bənövşəyi', 'Bənövşəyi'),
                       ('Boz', 'Boz'),
                       ('Çəhrayı', 'Çəhrayı'),
                       ('Göy', 'Göy'),
                       ('Gümüşü', 'Gümüşü'),
                       ('Mavi', 'Mavi'),
                       ('Narıncı', 'Narıncı'),
                       ('Qara', 'Qara'),
                       ('Qəhvəyi', 'Qəhvəyi'),
                       ('Qırmızı', 'Qırmızı'),
                       ('Qızılı', 'Qızılı'),
                       ('Sarı', 'Sarı'),
                       ('Tünd qırmızı', 'Tünd qırmızı'),
                       ('Yaş Asfalt', 'Yaş Asfalt'),
                       ('Yaşıl', 'Yaşıl')]

    colour = models.CharField(max_length=100, choices=COLOUR_CHOICES, default='Ağ')
    YEAR_CHOICES = []
    for r in range(1960, (datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))
    car_release_date = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
    description = models.TextField(max_length=5000, default='')
    # owner = models.ForeignKey(User, related_name='cars', on_delete=models.CASCADE, null=True)
    car_image = models.ImageField(upload_to='media/', blank=True)
    price = models.IntegerField('Qiymet', default=100)
    owner_name = models.CharField(max_length=100, default=None)
    # parsing azerbaijany cities for making dropdown menu

    owner_city = models.CharField(max_length=50, choices=CITY_CHOICES, default='Bakı')
    # owner_mail = models.EmailField()
    owner = models.ForeignKey(CustomUser, related_name='cars', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    moderate_on = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    image = models.FileField(blank=True, upload_to='media/')
    # class Meta:
    #     db_table = 'cars'

    # brand_name = models.CharField(max_length=100)
    # model_name = models.CharField(max_length=100)
    # BODY_TYPE_CHOICES = (
    #     ('sedan', "Sedan"),
    #     ('jeep', "Jeep"),
    #     ('offroad', "Offroad")
    # )
    # body_type = models.CharField(max_length=30,
    #                              choices=BODY_TYPE_CHOICES,
    #                              default='sedan')
    # min_price = models.IntegerField()
    # max_price = models.IntegerField()
    # YEAR_CHOICES = []
    # for r in range(1960, (datetime.now().year + 1)):
    #     YEAR_CHOICES.append((r, r))
    # car_release_min = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
    # car_release_max = models.IntegerField(choices=YEAR_CHOICES, default=datetime.now().year)
    # owner = models.ForeignKey(User, related_name='cars', on_delete=models.CASCADE, null=True)
