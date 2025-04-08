from django.test import TestCase, Client
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone


User = get_user_model()


class TestNotesList(TestCase):
    NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.no_author = User.objects.create(username='Не автор')
        cls.no_author_client = Client()
        cls.no_author_client.force_login(cls.no_author)
        author_notes = [
            Note(title=f'Заметка {index}', text='Просто текст.',
                 author=cls.author, slug=f'note_number_{index}')
            for index in range(10)
        ]
        Note.objects.bulk_create(author_notes)
        no_author_notes = [
            Note(title=f'Заметка {index}', text='Просто текст.',
                 author=cls.no_author, slug=f'nnote_number_{index}')
            for index in range(5)
        ]
        Note.objects.bulk_create(no_author_notes)

    def test_author_count_notes(self):
        response = self.author_client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, 10)

    def test_no_author_count_notes(self):
        response = self.no_author_client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, 5)


class TestNotes(TestCase):
    CREATE_NOTE_URL = reverse('notes:add')
    EDIT_NOTE_URL = 'notes:edit'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.no_author = User.objects.create(username='Не автор')
        cls.no_author_client = Client()
        cls.no_author_client.force_login(cls.no_author)
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст', author=cls.author, slug='note-1'
        )

    def test_note_in_context(self):
        url = reverse('notes:list')
        response = self.author_client.get(url)
        object_list = response.context.get('object_list', [])
        note_titles = [note.title for note in object_list]
        self.assertCountEqual(note_titles, [self.note.title])

    def test_no_other_user_notes(self):
        url = reverse('notes:list')
        response = self.author_client.get(url)
        object_list = response.context['object_list']
        authors_notes = Note.objects.filter(author=self.author)
        self.assertQuerysetEqual(object_list, authors_notes, transform=lambda x: x)

    def test_create_note_form_in_context(self):
        response = self.author_client.get(self.CREATE_NOTE_URL)
        self.assertIn('form', response.context)

    def test_edit_note_form_in_context(self):
        note = Note.objects.filter(author=self.author).first()
        edit_url = reverse(self.EDIT_NOTE_URL, kwargs={'slug': note.slug})
        response = self.author_client.get(edit_url)
        self.assertIn('form', response.context)
