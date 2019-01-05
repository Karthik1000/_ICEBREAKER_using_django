from django.db import models

# Create your models here.

class Testimony(models.Model):
    #objects = models.Manager()
    #published = PublishedManager()
    #published = models.Manager()

    name = models.CharField(max_length=120, blank=True)
    to_name = models.CharField(max_length=120,blank=True)
    commented = models.CharField(max_length=120, blank=True)
    #photo = models.ImageField(upload_to='tests/',null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updates = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name
