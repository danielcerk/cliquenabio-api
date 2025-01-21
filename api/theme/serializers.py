from rest_framework import serializers

from .models import ThemeGlobal, ThemeUser

class ThemeGlobalSerializer(serializers.ModelSerializer):

    class Meta:

        model = ThemeGlobal
        fields = '__all__'


class ThemeUserSerializer(serializers.ModelSerializer):

    class Meta:

        model = ThemeUser
        fields = '__all__'