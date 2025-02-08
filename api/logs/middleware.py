from django.utils import timezone, dateformat
from .models import UserLog
import json

class UserActivityLoggerMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        if request.body:

            try:

                request.data = json.loads(request.body.decode('utf-8') or "{}")

            except json.JSONDecodeError:

                request.data = {}

        response = self.get_response(request)

        if request.user.is_authenticated and not request.path.startswith("/static/"):

            action_details = self.get_action_details(request)

            if action_details:
                formatted_date = dateformat.format(
                    timezone.localtime(timezone.now()),
                    'H:i:s d-m-Y',
                )

                UserLog.objects.create(
                    user=request.user,
                    action=f"{action_details} às {formatted_date}"
                )

        return response

    def get_action_details(self, request):

        method = request.method
        object_id = None
        model_name = None

        try:

            if method in ["POST", "PUT", "PATCH", "DELETE"]:

                data = getattr(request, "data", request.POST or {})

                object_id = data.get("id") or data.get("pk") or None

                path_parts = request.path.strip("/").split("/")

                if len(path_parts) > 1 and path_parts[-1].isdigit():

                    object_id = path_parts[-1]
                    model_name = path_parts[-2]

                elif "change" in path_parts and len(path_parts) > 4:

                    object_id = path_parts[-2]
                    model_name = path_parts[-3]

                if method == "POST":

                    return f"Criou um novo {model_name or 'registro'} (ID: {object_id or 'N/A'})"
                
                elif method in ["PUT", "PATCH"]:

                    return f"Atualizou o {model_name or 'registro'} (ID: {object_id or 'N/A'})"
                
                elif method == "DELETE":

                    return f"Removeu o {model_name or 'registro'} (ID: {object_id or 'N/A'})"
        
        except json.JSONDecodeError:

            pass

        return None
