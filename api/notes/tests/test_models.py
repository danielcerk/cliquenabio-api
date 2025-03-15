from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from ..models import Note

User = get_user_model()

class NoteModelAPITestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            name="user1",
            email="admin@gmail.com",
            first_name="User",
            last_name="Ipsum",
            password="1234"
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_without_text(self):

        note = Note.objects.create(

            text=None,
            user=self.user

        )

        self.assertEqual(note.text, '"None"')

    def test_create_without_user(self):

        with self.assertRaises(Note.user.RelatedObjectDoesNotExist):
            
            Note.objects.create(text=None)

    def test_create_success(self):

        note = Note.objects.create(

            text='Olá, mundo!',
            user=self.user

        )

        self.assertEqual(note.text, '"Olá, mundo!"')
        self.assertIsNotNone(note.user)

