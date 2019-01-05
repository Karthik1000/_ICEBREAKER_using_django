from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add = True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    answer = models.TextField(max_length=300)

    def __str__(self):
        return self.answer
