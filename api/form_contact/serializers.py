from rest_framework import serializers

class FormContactEmailSerializer(serializers.Serializer):

    email = serializers.EmailField()
    content = serializers.CharField()