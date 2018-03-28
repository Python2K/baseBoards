from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Post, Topic, Board
from django.urls import reverse, resolvers
from ..views import PostUpdateView


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='haha')
        self.username='jon'
        self.password='dad123'
        self.user = User.objects.create_user(username=self.username,email='haha@163.com', password=self.password)
        self.topic = Topic.objects.create(subject='hello', board=self.board, starter=self.user)
        self.post = Post.objects.create(message='hhh', topic=self.topic, created_by=self.user)
        self.url = reverse('boards:edit_post', kwargs={
            'pk':self.board.pk,
            'topic_pk':self.topic.pk,
            'post_pk':self.post.pk,

        })


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('accounts:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnAuthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username='jjj'
        password='123'
        user = User.objects.create_user(username=username, email='jkj@163.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)