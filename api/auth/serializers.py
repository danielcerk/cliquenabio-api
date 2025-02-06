from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from api.profile_user.models import Profile
from api.firebase import FirebaseManager

from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod

    def get_token(cls, user):

        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True, validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    password = serializers.CharField(
        write_only=True, required=True, 
    )

    class Meta:

        model = User
        fields = ('name', 
            'first_name', 'last_name', 'email', 'password')


    def create(self, validated_data):

        user = User.objects.create(

            name = validated_data['name'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email = validated_data['email']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class AccountSerializer(serializers.ModelSerializer):

    biografy = serializers.CharField(
        write_only=False, 
        source='profile.biografy', 
        required=False, 
        allow_blank=True
    )

    image = serializers.CharField(
        write_only=True,
        source='profile.image',
        required=False
    )

    image_upload = serializers.ImageField(write_only=True, required=False)

    class Meta:

        model = User
        fields = ('id', 'name', 
            'first_name', 'last_name',
            'email', 'biografy', 'image', 'image_upload', 'password')

        extra_kwargs = {
            'name': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'password': {'required': False}
        }

    def update(self, instance, validated_data):

        profile_data = validated_data.pop('profile', {})
        biografy = profile_data.get('biografy', None)
        image_upload = validated_data.pop('image_upload', None)

        # Atualiza os campos do modelo User
        for attr in (
            'name', 'first_name', 'last_name', 'email', 'password'
            ):

            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])

        instance.save()

        try:
            
            profile = instance.profile

        except ObjectDoesNotExist:

            profile = Profile(by=instance)

        if image_upload:

            firebase_manager = FirebaseManager()
            destination_blob_name = f"image_profile/{image_upload.name}"
            image_url = firebase_manager.upload_image_to_storage(image_upload.read(), destination_blob_name)

            if image_url:
                profile.image = image_url

        if biografy is not None:
            
            profile.biografy = biografy

        profile.save()

        return instance