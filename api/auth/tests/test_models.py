from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from ..models import UserProfile

User = get_user_model()

class UserProfileAPITest(APITestCase):

    def setUp(self):

        pass