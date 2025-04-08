import pytest
from django.urls import reverse
from django.conf import settings
from news.forms import CommentForm


@pytest.mark.django_db
@pytest.mark.usefixtures('many_news')
def test_count_news_on_home_page(client):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('many_news')
def test_sorted_dates_on_home_page(client):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


@pytest.mark.django_db
@pytest.mark.usefixtures('news')
def test_sorted_dates_in_comments(client, news_id):
    response = client.get(reverse('news:detail', args=news_id))
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_fixture, expected_result',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), True),
    )
)
def test_pages_contains_form(client_fixture, expected_result, comment_id):
    url = reverse('news:detail', args=comment_id)
    response = client_fixture.get(url)
    assert ('form' in response.context) is expected_result
    if expected_result:
        assert isinstance(response.context['form'], CommentForm)
