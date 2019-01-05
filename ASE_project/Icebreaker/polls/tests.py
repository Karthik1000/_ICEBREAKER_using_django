from django.test import TestCase
from .models import *


class TestUrls(TestCase):

    def test_query_url(self):
        response = self.client.get('/polls/query/')
        self.assertEqual(response.status_code, 200)

    def test_sendmail_url(self):
        response = self.client.get('/polls/sendmail/')
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get('/polls/login/')
        self.assertEqual(response.status_code, 200)

    def test_adminpage_url(self):
        response = self.client.get('/polls/adminpage/')
        self.assertEqual(response.status_code, 200)

#model testing


class QuestionModelTest(TestCase):

    def test_string_representation(self):
        question = Question(question_text="My entry title")
        self.assertEqual(str(question), question.question_text)


class AnswerModelTest(TestCase):
    def test_name_representation(self):
        answer = Answer(answer="My answer")
        self.assertEqual(str(answer), answer.answer)
