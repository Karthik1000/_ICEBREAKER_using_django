from django.db import models
from django.contrib.auth.models import User
import datetime



class GroupTable(models.Model):
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=100, default="")
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    date = models.DateField(default=datetime.datetime.today)
    number = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default="")


    def __str__(self):
        return self.title

    def checkinggroup(self):
        return '%s' % (self.title)


class MemberTable(models.Model):
    group = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s by %s' % (self.group, self.user)

class CommentTable(models.Model):
    group = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=500)


    def __str__(self):
        return u'on %s by %s said    %s' % (self.group, self.user, self.comment)

    def checkingcomment(self):
        return '%s' % (self.group.title)

class UpdateTable(models.Model):
    group = models.ForeignKey(GroupTable, on_delete=models.CASCADE)
    update = models.CharField(max_length=1000)
    #date = models.DateField(default=datetime.date.today())
    def __str__(self):
        return u'%s' % (self.update)

    def checkingupdate(self):
        return '%s' % (self.update)

