from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from ..serializers import NoteSerializer

User = get_user_model()

class NoteSerializerAPITestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            name="user1",
            email="admin@gmail.com",
            first_name="User",
            last_name="Ipsum",
            password="1234"
        )

        self.client.force_authenticate(user=self.user)

        self.url = "/api/v1/account/me/note/"

        get_user = User.objects.get(name='user1')

        self.data = {

            'text': 'Olá, Mundo!',
            'user': get_user.id

        }

    def test_create_note_without_text(self):

        data = self.data.copy()
        del data["text"]

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_note_success(self):

        data = self.data.copy()

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)