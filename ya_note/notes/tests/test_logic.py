from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note
from pytils.translit import slugify

User = get_user_model()


class TestNoteCreation(TestCase):
    TEXT_NOTE = 'Текст заметки'
    TITLE_NOTE = 'Титул заметки'
    SLUG_NOTE = 'primer'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.url = reverse('notes:add')
        cls.form_data = {'title': cls.TITLE_NOTE, 'text': cls.TEXT_NOTE}
        cls.note = Note.objects.create(title=cls.TEXT_NOTE,
                                       text=cls.TITLE_NOTE,
                                       author=cls.author,
                                       slug=cls.SLUG_NOTE)
        cls.slug_data = {'title': cls.TITLE_NOTE,
                         'text': cls.TEXT_NOTE,
                         'slug': cls.SLUG_NOTE}

    def test_anonymous_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_authuser_create_note(self):
        self.auth_client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)

    def test_create_note_with_not_unique_slug(self):
        self.client.post(self.url, data=self.slug_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_create_without_slug(self):
        self.auth_client.post(self.url, data=self.form_data)
        note = Note.objects.get(id=2)
        slug_note = note.slug
        print(slug_note)
        print(slugify(note.title))
        self.assertEqual(slug_note, slugify(note.title))


class TestNoteDeleteEdit(TestCase):
    TITLE_NOTE = 'Титул заметки'
    TEXT_NOTE = 'Текст заметки'
    NEW_TEXT_NOTE = 'Новый текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.no_author = User.objects.create(username='Не автор')
        cls.no_author_client = Client()
        cls.no_author_client.force_login(cls.no_author)
        cls.note = Note.objects.create(
            title=cls.TITLE_NOTE, text=cls.TEXT_NOTE, author=cls.author
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {'title': cls.TITLE_NOTE, 'text': cls.NEW_TEXT_NOTE}
        cls.success = reverse('notes:success')

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_no_author_cant_delete_note(self):
        response = self.no_author_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_TEXT_NOTE)

    def test_no_author_cant_edit_note(self):
        response = self.no_author_client.post(self.edit_url,
                                              data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.TEXT_NOTE)
