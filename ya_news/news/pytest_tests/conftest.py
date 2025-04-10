import pytest
from django.conf import settings
from django.test.client import Client
from news.models import News, Comment
from news.forms import BAD_WORDS


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Название новости',
        text='Текст новости',
    )
    return news


@pytest.fixture
def many_news():
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        all_news.append(News(title=f"Новость {index}",
                             text="Текст новости"))
    return News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def news_id(news):
    return (news.id,)


@pytest.fixture
def comment_id(comment):
    return (comment.id,)


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }


@pytest.fixture
def form_data_bad_word():
    return {
        'text': BAD_WORDS[0]
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
