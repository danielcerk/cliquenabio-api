from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Profile

class ProfileSerializer(ModelSerializer):

    owner = serializers.CharField(
        source='by.name', read_only=True
    )

    full_name = serializers.CharField(
        source='by.full_name', read_only=True
    )

    class Meta:

        model = Profile
        fields = [
            'by', 'owner', 'full_name',
            'first_name', 'last_name',
            'image', 'banner', 'slug', 'biografy'
        ]