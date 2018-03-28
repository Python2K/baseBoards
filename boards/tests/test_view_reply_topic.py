from django.test import TestCase
from ..models import Board, Post, Topic
from django.contrib.auth.models import User


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='django', description='test')
        self.username = 'django'
        self.password = 'django123'
        self.user = User.objects.create_user(username=self.username, email='das@163.con', password=self.password)
        self.topic = Topic.objects.create(subject='hellloword', board=self.board, starter=self.user)
        Post.objects.create(message='helloword', topic=self.topic, created_by=self.user)

# class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
#     # ...
#
#
# class ReplyTopicTests(ReplyTopicTestCase):
#     # ...
#
#
# class SuccessfulReplyTopicTests(ReplyTopicTestCase):
#     # ...
#
# class InvalidReplyTopicTests(ReplyTopicTestCase):
#     # ...