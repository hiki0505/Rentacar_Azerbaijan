from django.contrib import admin

# Register your models here.
from .models import Car, BrandName, ModelName, CarImage


# class CarCategory()


class CarImagesInline(admin.TabularInline):
    model = CarImage


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    readonly_fields = ["createdAt", "updatedAt"]
    list_display = ("brand_name", "model_name", "body_type", "fuel_type", "mileage",
                    "colour", "car_release_date", "description", "car_image", "price",
                    "owner_name", "owner_city", "owner", "createdAt", "updatedAt")
    inlines = [
        CarImagesInline,
    ]


# admin.site.register(Car)
admin.site.register(BrandName)
admin.site.register(ModelName)
admin.site.register(CarImage)
