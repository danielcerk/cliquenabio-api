from rest_framework import serializers

from .models import FormContactEmail

class FormContactEmailSerializer(serializers.ModelSerializer):

    class Meta:

        model = FormContactEmail
        fields = '__all__'

class ContactEmailSerializer(serializers.Serializer):

    email = serializers.EmailField()
    content = serializers.CharField()