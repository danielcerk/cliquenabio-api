from rest_framework import serializers

from .models import Product
from api.firebase import FirebaseManager

class ProductSerializer(serializers.ModelSerializer):

    owner = serializers.CharField(
        source='created_by.name', read_only=True
    )
    image_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:

        model = Product
        fields = ['id', 'name', 'small_description', 
                  'owner', 'image', 'image_upload',
                    'created_by', 'created_at']
        
        extra_kwargs = {
            'created_by': {'required': False},
        }

    def create(self, validated_data):

        image_upload = validated_data.pop('image_upload', None)
        product = Product(**validated_data)

        if image_upload:

            firebase_manager = FirebaseManager()
            destination_blob_name = f"images/{image_upload.name}"
            image_url = firebase_manager.upload_image_to_storage(image_upload.read(), destination_blob_name)

            if image_url:

                product.image = image_url

        product.save()

        return product

    def update(self, instance, validated_data):

        image_upload = validated_data.pop('image_upload', None)

        
        if 'created_by' in validated_data:

            instance.created_by = validated_data['created_by']


        for attr, value in validated_data.items():

            if attr != 'created_by':

                setattr(instance, attr, value)

        if image_upload:

            firebase_manager = FirebaseManager()
            destination_blob_name = f"images/{image_upload.name}"
            image_url = firebase_manager.upload_image_to_storage(image_upload.read(), destination_blob_name)

            if image_url:
                
                instance.image = image_url

        instance.save()

        return instance