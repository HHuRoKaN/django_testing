from django.test import TestCase, Client
from django.contrib.auth import get_user_model


User = get_user_model()


class TestBase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.no_author = User.objects.create(username='Не автор')
        cls.no_author_client = Client()
        cls.no_author_client.force_login(cls.no_author)
