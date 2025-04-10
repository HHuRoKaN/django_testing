from pytest_django.asserts import assertRedirects
from django.urls import reverse
from news.models import Comment
import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from news.forms import WARNING
from pytils.translit import slugify
from http import HTTPStatus

@pytest.mark.parametrize(
    'need_data, count_objects',
    (
        (pytest.lazy_fixture('form_data'), 1),
        (pytest.lazy_fixture('form_data_bad_word'), 0),
    )
)
def test_user_can_create_comment_without_bad_words(
    author_client, author, need_data, news_id, count_objects
):
    url = reverse('news:detail', args=news_id)
    response = author_client.post(url, data=need_data)
    assert Comment.objects.count() == count_objects
    if Comment.objects.count() == 1:
        assertRedirects(response, f'{url}#comments')
        comment = Comment.objects.get()
        assert comment.text == need_data['text']
        assert comment.author == author
    else:
        assertFormError(response, form='form', field='text', errors=WARNING)


def test_anonymous_user_cant_create_comment(client, form_data, news_id):
    url = reverse('news:detail', args=news_id)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


@pytest.mark.usefixtures('comment')
@pytest.mark.parametrize(
    'parametrized_client, expected_status, expected_count_comments',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND, 1),
        (pytest.lazy_fixture('author_client'), HTTPStatus.FOUND, 0)
    ),
)
def test_delete_comment(
    parametrized_client, expected_status, comment_id, expected_count_comments
):
    response = parametrized_client.delete(
        reverse('news:delete', args=comment_id))
    comments_count = Comment.objects.count()
    assert response.status_code == expected_status
    assert expected_count_comments == comments_count
    if response.status_code == HTTPStatus.FOUND:
        assertRedirects(response,
                        reverse('news:detail', args=comment_id) + '#comments')



@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.FOUND),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND)
    ),
)
def test_edit_comment(
    parametrized_client, expected_status, form_data, comment_id, comment
):
    edit_url = reverse('news:edit', args=comment_id)
    response = parametrized_client.post(edit_url, data=form_data)
    assert response.status_code == expected_status
    comment.refresh_from_db()
    if response.status_code == HTTPStatus.FOUND:
        assertRedirects(response,
                        reverse('news:detail', args=comment_id) + '#comments')
        assert comment.text == form_data['text']
