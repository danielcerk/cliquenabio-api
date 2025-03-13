from rest_framework import serializers

from .models import Note

class NoteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Note
        fields = [

            'id', 'text', 'user', 'created_at', 'updated_at'

        ]
        
        extra_kwargs = {
            
            'user': {'required': False},

        }

    def update(self, instance, validated_data):

        if 'user' in validated_data:

            instance.user = validated_data['user']


        for attr, value in validated_data.items():

            if attr != 'user':

                setattr(instance, attr, value)

        instance.save()

        return instance