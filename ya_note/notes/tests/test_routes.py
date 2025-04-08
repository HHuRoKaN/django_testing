from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Создатель заметок')
        cls.reader = User.objects.create(username='Другой пользователь')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', author=cls.author
        )

    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_authuser(self):
        urls = ('notes:list', 'notes:success', 'notes:add')
        self.client.force_login(self.author)
        for name in urls:
            with self.subTest(user=self.author, name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_note(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
            (None, HTTPStatus.FOUND),
        )
        for user, status in users_statuses:
            if user:
                self.client.force_login(user)
            else:
                self.client.logout()
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name in (
            'notes:edit', 'notes:delete', 'notes:detail',
                'notes:list', 'notes:success'):
            with self.subTest(name=name):
                if name in ('notes:list', 'notes:success'):
                    url = reverse(name)
                else:
                    url = reverse(name, args=(self.note.slug,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
