from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection
from .serializers import StatusSerializer


# QUantidade de momentos criados por dia
# Quantidade de links criados por dia

User = get_user_model()

class StatusView(APIView):

    def get(self, request, *args, **kwargs):

        try:

            connection.ensure_connection()
            status_app, status_db = True, True

        except Exception:

            status_app, status_db = False, False

        data = {
            "status_app":  status_app,
            "status_db": status_db,
        }

        serializer = StatusSerializer(data)

        return Response(serializer.data)
    