from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Temp(models.Model):
    temp_user = models.CharField(max_length=30,default='')
    otp = models.CharField(max_length=6,default='')
    #num = models.IntegerField(max_length=1,default=0)

    def __str__(self):
        return self.temp_user

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/',null=True, blank=True)
    dob = models.DateTimeField(auto_now_add=True,null=True)
    github_link = models.URLField(max_length=200,null=True)
    facebook_link = models.URLField(max_length=200,null=True)
    linkedIn_link = models.URLField(max_length=200,null=True)
    #email_confirmed = models.BooleanField(default=False)
    # other fields...
    def __str__(self):
        return "Profile {}".format(self.user.username)
