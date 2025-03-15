from rest_framework.test import APITestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from ..models import Link

User = get_user_model()

class LinkModelAPITestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            name="user1",
            email="admin@gmail.com",
            first_name="User",
            last_name="Ipsum",
            password="1234"
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_without_url(self):

        with self.assertRaises(ValueError):
            
            Link.objects.create(url=None)

    def test_create_without_created_by(self):

        with self.assertRaises(Link.created_by.RelatedObjectDoesNotExist):
            
            Link.objects.create(url='https://cliquenabio.com.br/')

    def test_create_success(self):

        link = Link.objects.create(

            url='https://cliquenabio.com.br/',
            created_by=self.user

        )

        self.assertIsNotNone(link.created_by)

