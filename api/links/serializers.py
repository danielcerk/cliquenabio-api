from rest_framework import serializers

from .models import Link

class LinkSerializer(serializers.ModelSerializer):

    owner = serializers.CharField(
        source='created_by.name', read_only=True
    )

    class Meta:

        model = Link
        fields = ['owner', 'url', 'social_network',
             'username', 'created_by', 
             'created_at', 'updated_at']
        
        extra_kwargs = {

            'created_by': {'required': False},

        }

    def update(self, instance, validated_data):

        if 'created_by' in validated_data:

            instance.created_by = validated_data['created_by']


        for attr, value in validated_data.items():

            if attr != 'created_by':

                setattr(instance, attr, value)

        instance.save()

        return instance

