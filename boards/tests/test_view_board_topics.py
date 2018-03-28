from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls import resolve

from boards.forms import NewTopicForm
from boards.models import Board, Topic, Post
# from boards.views import home, board_topics, new_topic
from boards.views import TopicListView
class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name="django", description='django board.')

    def test_board_topics_view_status_code(self):
        url = reverse('boards:board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_tpoics_view_not_found_status_code(self):
        url = reverse('boards:board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_link_back_to_homepags(self):
        url = reverse('boards:board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        homepags_url = reverse('boards:home')
        self.assertContains(response, 'href="{0}"'.format(homepags_url))

    def test_board_topics_view_contains_new_topic_view(self):
        new_topic_url = reverse('boards:new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('boards:board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))