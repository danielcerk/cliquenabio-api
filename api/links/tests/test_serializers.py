from rest_framework.test import APITestCase
from rest_framework import status

from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from ..serializers import LinkSerializer


User = get_user_model()

class LinkSerializerAPITestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            name="user1",
            email="admin@gmail.com",
            first_name="User",
            last_name="Ipsum",
            password="1234"
        )

        self.client.force_authenticate(user=self.user)

        self.url = "/api/v1/account/me/link/"

        get_user = User.objects.get(name='user1')

        self.data = {

            'url': 'https://cliquenabio.com.br/',
            'user': get_user.id

        }

    def test_create_link_without_url(self):

        data = self.data.copy()
        del data["url"]

        with self.assertRaises(IntegrityError):

            response = self.client.post(self.url, data, format="json")

    def test_create_link_success(self):

        data = self.data.copy()

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)