from rest_framework import serializers

from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:

        model = Feedback
        fields = '__all__'

        extra_kwargs = {
            'user': {'required': False}
        }