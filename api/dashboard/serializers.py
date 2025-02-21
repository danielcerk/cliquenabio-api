from rest_framework import serializers

from api.logs.models import UserLog
from api.analytics.models import AnalyticProfileViewsPerDate
from api.snaps.models import Snap
from api.links.models import Link

from django.db import models
from django.db.models import Sum

from datetime import datetime, timedelta

class DashboardSerializer(serializers.Serializer):

    views = serializers.IntegerField(source='analyticprofileviews.number')
    count_views_per_date = serializers.SerializerMethodField()
    snaps_count = serializers.CharField(source='snapcount.number')
    links_count = serializers.CharField(source='linkcount.number')
    user = serializers.CharField(source='name')
    logs = serializers.SerializerMethodField()

    class Meta:

        fields = ['views', 'count_views_per_date', 
            'snaps_count', 'links_count', 'user', 'logs']

    def get_logs(self, instance):

        logs = UserLog.objects.filter(user=instance).order_by("-timestamp")[:5]
        return [{"action": log.action, "timestamp": log.timestamp} for log in logs]

    def get_count_views_per_date(self, instance):

        views_per_date = (
            AnalyticProfileViewsPerDate.objects
            .filter(owner=instance)
            .values("created_at__date")
            .annotate(total_views=models.Sum("number"))
            .order_by("created_at__date")
        )        

        views_dict = {view["created_at__date"]: view["total_views"] for view in views_per_date}

        max_date = datetime.today().date()
        min_date = max_date - timedelta(days=7)

        complete_views = {}
        current_date = min_date

        while current_date <= max_date:
            
            formatted_date = current_date.strftime('%d/%m')
            complete_views[formatted_date] = views_dict.get(current_date, 0)
            current_date += timedelta(days=1)

        return complete_views

class AdminDashboardSerializer(serializers.Serializer):

    views = serializers.SerializerMethodField()
    count_views_per_date = serializers.SerializerMethodField()
    snaps_count = serializers.SerializerMethodField()
    links_count = serializers.SerializerMethodField()

    # Is logs

    actions = serializers.SerializerMethodField()

    class Meta:

        fields = [
            'views', 'count_views_per_date',
            'snaps_count', 'links_count', 'actions'
        ]

    def get_views(self, instance):

        total_views = AnalyticProfileViewsPerDate.objects.aggregate(total=Sum("number"))["total"]

        return total_views or 0
    
    def get_snaps_count(self, instance):

        total_snaps = Snap.objects.aggregate(total=Sum("created_by"))["total"]

        return total_snaps or 0
    
    def get_links_count(self, instance):

        total_links = Link.objects.aggregate(total=Sum("created_by"))["total"]

        return total_links or 0
    
    def get_actions(self, instance):

        actions = UserLog.objects.aggregate(total=Sum("user"))["total"]

        return actions or 0
    
    def get_count_views_per_date(self, instance):

        views_per_date = (
            AnalyticProfileViewsPerDate.objects
            .values("created_at__date")
            .annotate(total_views=models.Sum("number"))
            .order_by("created_at__date")
        )

        return {str(view["created_at__date"]): view["total_views"] for view in views_per_date}