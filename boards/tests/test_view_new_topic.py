from django.test import TestCase


class LoginRequiredNewTopicTexts(TestCase):
    def setUp(self):
        Board.objects.create(name='django', description='testlogin')
        self.url = reverse('boards:new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('accounts:login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve

from boards.forms import NewTopicForm
from boards.models import Board, Topic, Post
from boards.views import new_topic


# Create your tests here.






class NewTopicTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name="Django test", description="Test django")
        self.pk = self.board.pk
        url = reverse('boards:new_topic', kwargs={'pk': self.pk})
        self.response = self.client.get(url)

    def test_new_topic_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('boards:new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolve_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        url = reverse('boards:board_topics', kwargs={'pk': self.pk})
        self.assertContains(self.response, 'href="{0}"'.format(url))


class NewTopicTest(TestCase):
    def setUp(self):
        Board.objects.create(name='django', description='django test')
        User.objects.create_user(username='test', email='123@1.com', password='123')
        self.client.login(username='test', password='123')

    def test_scrf(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'test',
            'message': 'message',
        }
        response = self.client.post(url, data=data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        # 如果无效数据应该不redirect
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_empty_fields(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': '',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('boards:new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
