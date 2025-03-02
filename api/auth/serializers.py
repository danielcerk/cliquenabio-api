from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from api.subscriptions.models import *
from api.profile_user.models import Profile
from api.firebase import FirebaseManager

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

from datetime import datetime

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
            'first_name', 'last_name', 
            'email', 'password', 'terms_of_use_is_ready')


    def create(self, validated_data):

        user = User.objects.create(

            name = validated_data['name'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email = validated_data['email'],
            terms_of_use_is_ready=validated_data['terms_of_use_is_ready']

        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
class AccountSerializer(serializers.ModelSerializer):

    plan = serializers.CharField(
        source='subscription.plan.name', read_only=True
    )

    biografy = serializers.CharField(
        write_only=False, 
        source='profile.biografy', 
        required=False, 
        allow_blank=True
    )

    image = serializers.CharField(
        source='profile.image',
        required=False
    )

    banner = serializers.CharField(
        source='profile.banner',
        required=False
    )

    image_upload = serializers.ImageField(write_only=True, required=False)
    banner_upload = serializers.ImageField(write_only=True, required=False)

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'id', 'name', 
            'first_name', 'last_name',
            'email', 'biografy', 'image', 
            'image_upload', 'banner', 'banner_upload',
            'password', 'plan'
        )

        extra_kwargs = {
            'name': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'password': {'required': False},
        }

    def update(self, instance, validated_data):

        profile_data = validated_data.pop('profile', {})
        biografy = profile_data.get('biografy', None)
        image_upload = validated_data.pop('image_upload', None)
        banner_upload = validated_data.pop('banner_upload', None)

        password = validated_data.pop("password", None)

        firebase_manager = FirebaseManager()

        if password:

            instance.password = make_password(password)

        for attr in (
            'name', 'first_name', 'last_name', 'email'):

            if attr in validated_data:

                setattr(instance, attr, validated_data[attr])

        instance.save()

        try:

            profile = instance.profile

        except ObjectDoesNotExist:

            profile = Profile(by=instance)

        if image_upload:

            destination_blob_name = f"image_profile/{image_upload.name}"
            image_url = firebase_manager.upload_image_to_storage(image_upload.read(), destination_blob_name)

            if image_url:

                profile.image = image_url

        if banner_upload:

            destination_blob_name = f"banner_profile/{banner_upload.name}"
            banner_url = firebase_manager.upload_image_to_storage(banner_upload.read(), destination_blob_name)

            if banner_url:

                profile.banner = banner_url

        if biografy is not None:

            profile.biografy = biografy

        profile.save()

        subscription = instance.subscription

        if subscription and subscription.cancel_at_period_end:

            current_time = datetime.now()

            if subscription.current_period_end < current_time:

                subscription.plan = Plans.objects.get(name='GRÁTIS')

                subscription.save()

        return instance