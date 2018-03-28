from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Board,Topic,Post
# from ..views import topic_posts
from ..views import PostListView
from django.contrib.auth.models import User

class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='django', description='hello')
        user = User.objects.create_user(username='test1', email='test1@163.com', password='test123')
        topic = Topic.objects.create(subject='test1',starter=user, board=board)
        url = reverse('boards:topic_posts', kwargs={'pk': board.pk, 'topic_pk':topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)
