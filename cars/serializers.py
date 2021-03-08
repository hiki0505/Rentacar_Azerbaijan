import datetime

from rest_framework import serializers
from cars.models import Car, BrandName, ModelName, CarImage


class BrandnameSerializer(serializers.ModelSerializer):
    # brand_name = serializers.SlugRelatedField(slug_field="name", read_only=True)
    # model_name = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = BrandName
        fields = '__all__'


class ModelnameSerializer(serializers.ModelSerializer):
    # brandname = serializers.SlugRelatedField(slug_field="brandname", queryset=BrandName.objects.all())
    # brandname = serializers.RelatedField(BrandName.objects.all())
    # brandname = serializers.StringRelatedField()

    # def create(self, validated_data):
    #     return ModelName.objects.create(
    #         id=validated_data['brandname']['id'],
    #         name=validated_data['name'],
    #         brandname=validated_data['brandname']['brandname']
    #     )
    # def to_representation(self, instance):
    #     rep = super(ModelnameSerializer, self).to_representation(instance)
    #     # rep['brand_name'] = BrandnameSerializer(instance.brand_name).data
    #     # rep['model_name'] = ModelnameSerializer(instance.model_name).data
    #     rep['brandname'] = instance.brandname.brandname
    #     return rep

    class Meta:
        model = ModelName
        fields = '__all__'

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('id', 'car', 'image')


class CarSerializer(serializers.ModelSerializer):
    # brand_name = serializers.SerializerMethodField()
    # model_name = serializers.SerializerMethodField()
    # brand_name = serializers.SlugRelatedField(slug_field="brandname", queryset=BrandName.objects.all())
    # model_name = serializers.SlugRelatedField(slug_field="name", queryset=ModelName.objects.all())
    # brand_ser = BrandnameSerializer(source='brand_name')
    # model_ser = ModelnameSerializer(source='model_name')
    # brands = serializers.StringRelatedField()
    # modelnames = serializers.StringRelatedField()
    # brandnames = BrandnameSerializer(read_only=True, many=True)
    # modelnames = ModelnameSerializer(read_only=True, many=True)
    # brand_name = serializers.StringRelatedField(slug_field="brandname", read_only=True)
    # model_name = serializers.StringRelatedField(slug_field="name", read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    carimage_set = CarImageSerializer(allow_null=True, many=True, required=False)

    class Meta:
        model = Car
        # fields = '__all__'
        exclude = ('moderate_on', )
        extra_kwargs = {'createdAt': {'read_only': True}, 'updatedAt': {'read_only': True}}


    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        car = Car.objects.create(**validated_data)
        for image_data in images_data.getlist('image'):
            CarImage.objects.create(car=car, image=image_data)
        return car

    def clear_existing_images(self, instance):
        for car_image in instance.carimage_set.all():
            car_image.image.delete()
            car_image.delete()

    def update(self, instance, validated_data):
        # instance.updatedAt = datetime.datetime.now()
        images = self.context.get('view').request.FILES
        print(images)
        if images:
            self.clear_existing_images(instance)  # uncomment this if you want to clear existing images.
            post_image_model_instance = [CarImage(car=instance, image=image) for image in images.getlist('image')]
            CarImage.objects.bulk_create(
                post_image_model_instance
            )
        # instance.save()
        return super().update(instance, validated_data)
        # fields = ('brand_ser',  'model_ser', 'body_type', 'fuel_type', 'mileage', 'car_release_date', 'description', 'price', 'owner')
        # extra_kwargs = {'owner': {'read_only': True}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['brand_name'] = BrandnameSerializer(instance.brand_name).data
        # rep['model_name'] = ModelnameSerializer(instance.model_name).data
        rep['brand_name'] = instance.brand_name.brandname
        rep['model_name'] = instance.model_name.name
        return rep

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     # rep['brand_name'] = BrandnameSerializer(instance.brand_name).data
    #     # rep['model_name'] = ModelnameSerializer(instance.model_name).data
    #     rep['brand_name'] = instance.brand_name.brandname
    #     rep['model_name'] = instance.model_name.name
    #     return rep
