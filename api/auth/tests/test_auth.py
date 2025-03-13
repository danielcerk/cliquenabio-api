from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()

# How to run: python manage.py test api.auth

class UserProfileAPITest(APITestCase):

    def setUp(self):

        self.url = "/api/v1/auth/register/"

        self.data = {

            'name': 'user1',
            'email': 'admin@gmail.com',
            'first_name': 'User',
            'last_name': 'Ipsum',
            'password': '1234',
            'terms_of_use_is_ready': True,

        }

    def test_create_user_without_name(self):

        data = self.data.copy()
        del data["name"]

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_create_user_without_email(self):

        data = self.data.copy()
        del data["email"]

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)    

    def test_create_user_without_password(self):

        data = self.data.copy()
        del data["password"]

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data) 

    def test_create_user_without_firstname_and_lastname(self):

        data = self.data.copy()
        del data["first_name"]
        del data["last_name"]

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("first_name", response.data) 
        self.assertIn("last_name", response.data)

    def test_create_user_success(self):

        data = self.data.copy()

        response = self.client.post(self.url, data, format="json")

        self.user = User.objects.get(email=self.data["email"])
        
        self.client.force_authenticate(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


