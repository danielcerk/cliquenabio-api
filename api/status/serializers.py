from rest_framework import serializers
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model
from .utils import GetAttributes

from ..links.models import Link
from ..product.models import Product

User = get_user_model()

class StatusSerializer(serializers.Serializer):

    count_user_per_data = serializers.DictField()

    count_links_per_data = serializers.DictField()
    count_moments_per_data = serializers.DictField()
    
    status_app = serializers.BooleanField(default=False)
    status_db = serializers.BooleanField(default=False)
    count_users = serializers.IntegerField()
    contribuitors = serializers.ListField(
        child=serializers.DictField()
    )

    def to_representation(self, instance):
       
        get_all_users_count = (

            User.objects.annotate(data=TruncDate('created_at'))
            .values('data')
            .annotate(total=Count('id'))
            .order_by('data')
            
        )

        count_users_per_data = {
            obj['data'].strftime("%d/%m"): obj['total'] for obj in get_all_users_count
        }

        get_all_links_count = (

            Link.objects.annotate(data=TruncDate('created_at'))
            .values('data')
            .annotate(total=Count('id'))
            .order_by('data')
            
        )

        count_links_per_data = {
            obj['data'].strftime("%d/%m"): obj['total'] for obj in get_all_links_count
        }

        get_all_moments_count = (

            Product.objects.annotate(data=TruncDate('created_at'))
            .values('data')
            .annotate(total=Count('id'))
            .order_by('data')
            
        )

        count_moments_per_data = {
            obj['data'].strftime("%d/%m"): obj['total'] for obj in get_all_moments_count
        }

        count_users = User.objects.all().count()
        contribuitors_users = GetAttributes().get_contribuitors()

        # Recuperar valores de status
        status_app = instance.get('status_app', False)
        status_db = instance.get('status_db', False)

        # Retornar todos os campos
        return {
            'count_user_per_data': count_users_per_data,
            'count_links_per_data': count_links_per_data,
            'count_moments_per_data': count_moments_per_data,
            'status_app': status_app,
            'status_db': status_db,
            'count_users': count_users,
            'contribuitors': contribuitors_users,
        }