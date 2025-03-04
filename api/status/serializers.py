from rest_framework import serializers
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from ..links.models import Link
from ..snaps.models import Snap
from .utils import GetAttributes

from collections import OrderedDict

User = get_user_model()

class StatusSerializer(serializers.Serializer):
    
    count_user_per_date = serializers.DictField()
    count_links_per_date = serializers.DictField()
    count_snaps_per_date = serializers.DictField()

    status_app = serializers.BooleanField(default=False)
    status_db = serializers.BooleanField(default=False)
    count_users = serializers.IntegerField()
    contribuitors = serializers.ListField(child=serializers.DictField())

    def fill_missing_dates(self, data_dict):

        max_date = datetime.today().date()
        min_date = max_date - timedelta(days=6)

        complete_data = OrderedDict()

        current_date = min_date

        while current_date <= max_date:
            
            formatted_date = current_date.strftime("%d/%m")
            complete_data[formatted_date] = data_dict.get(formatted_date, 0)
            current_date += timedelta(days=1)

        return complete_data

    def to_representation(self, instance):

        get_all_users_count = (
            User.objects.annotate(data=TruncDate('created_at'))
            .values('data')
            .annotate(total=Count('id'))
            .order_by('data')
        )
        count_users_per_date = OrderedDict(
            (obj['data'].strftime("%d/%m"), obj['total']) for obj in get_all_users_count
        )

        get_all_links_count = (
            Link.objects.annotate(data=TruncDate('created_at'))
            .values('data')
            .annotate(total=Count('id'))
            .order_by('data')
        )
        count_links_per_date = OrderedDict(
            (obj['data'].strftime("%d/%m"), obj['total']) for obj in get_all_links_count
        )

        get_all_snaps_count = (
            Snap.objects.annotate(data=TruncDate('created_at'))
            .values('data')
            .annotate(total=Count('id'))
            .order_by('data')
        )
        count_snaps_per_date = OrderedDict(
            (obj['data'].strftime("%d/%m"), obj['total']) for obj in get_all_snaps_count
        )

        count_users = User.objects.all().count()
        contribuitors_users = GetAttributes().get_contribuitors()

        status_app = instance.get('status_app', False)
        status_db = instance.get('status_db', False)

        count_users_per_date = self.fill_missing_dates(count_users_per_date)
        count_links_per_date = self.fill_missing_dates(count_links_per_date)
        count_snaps_per_date = self.fill_missing_dates(count_snaps_per_date)

        return {
            'count_user_per_date': count_users_per_date,
            'count_links_per_date': count_links_per_date,
            'count_snaps_per_date': count_snaps_per_date,
            'status_app': status_app,
            'status_db': status_db,
            'count_users': count_users,
            'contribuitors': contribuitors_users,
        }
