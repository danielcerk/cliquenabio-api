from rest_framework import serializers
from .models import UserTheme  # Importe o novo modelo

class UserThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTheme
        fields = [
            'background_color',
            'foreground_color', 
            'font_family',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']  

    def create(self, validated_data):

        user = self.context['request'].user
        if UserTheme.objects.filter(user=user).exists():
            raise serializers.ValidationError("Este usuário já possui um tema registrado")
        
        return UserTheme.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):

        instance.background_color = validated_data.get('background_color', instance.background_color)
        instance.foreground_color = validated_data.get('foreground_color', instance.foreground_color)
        instance.font_family = validated_data.get('font_family', instance.font_family)
        instance.save()
        return instance