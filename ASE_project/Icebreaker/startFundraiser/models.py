from django.db import models
from django.db.models import PROTECT
from django.utils import timezone
import datetime
from datetime import timedelta
from PIL import Image
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

from django.core.exceptions import ValidationError

choose_from_categories = (
    ('creative', (
        ('comics', 'comics'),
        ('art', 'art'),
    )),
    ('tech', (
        ('education', 'education'),
        ('phones', 'phones'),
    )),
    ('community', (
        ('environment', 'environment'),
        ('culture', 'culture'),
    ))
)

campaign_choices = (
    ('created', 'Campaign Created'),
    ('started', 'Campaign Started'),
    ('successfully', 'Campaign Ended Successfully'),
    ('unsuccessfully', 'Campaign Ended Unsuccesfully'),
)


def validate_tags(value):
    if ',' in value:
        return value
    else:
        raise ValidationError("Enter comma seperated tags")


class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_Title = models.CharField(max_length=200, unique=True)
    campaign_Tagline = models.CharField(max_length=200)
    campaign_Card_Image = models.ImageField(blank=True, null=True)
    campaign_Category = models.CharField(
        max_length=20,
        choices=choose_from_categories,
    )
    country = models.CharField(max_length=50, default='India')
    city = models.CharField(max_length=50)
    image = models.ImageField(upload_to="media")
    video = models.ImageField(upload_to="media", blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True, validators=[validate_tags])
    overview = models.TextField(max_length=500)
    story = models.TextField(max_length=500, blank=True, null=True)
    goal = models.FloatField()
    start_Date = models.DateField()
    end_Date = models.DateField()
    pledged = models.FloatField(default=0.0)
    people_pledged = models.IntegerField(default=0)
    campaign_status = models.CharField(max_length=120, choices=campaign_choices, default='created')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    views = models.IntegerField(default=0)
    date_created = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    perks = models.BooleanField(default=False)

    def __str__(self):
        return self.campaign_Title

    def duration_of_campaign(self):
        return self.end_Date - self.start_Date

    def get_absolute_url(self):
        return reverse('startFundraiser:campaign_detail', args=[self.id])

    def total_likes(self):
        return self.likes.count()


class Reward(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amount = models.FloatField()
    perks = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    claimed = models.PositiveIntegerField(default=0, blank=True, null=True)
    delivery = models.BooleanField(default=False)

    def __str__(self):
        return str(self.campaign)
    def check_reward(self):
        return '%s' % self.perks


class RewardClaimed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward =  models.ForeignKey(Reward, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
    def check_rewardclaimed(self):
        return '%s' % self.reward



class Faqs(models.Model):
    class Meta:
        verbose_name_plural = 'FAQs'

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    question = models.TextField(max_length=100, default='What are you raising funds for?')
    answer = models.TextField(max_length=200, default='Its for a good cause')

    def __str__(self):
        return self.question

    def check_faq(self):
        return '%s' % self.question

    class Meta:
        verbose_name_plural = "faqs"


class Update(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Post(models.Model):
    title = models.CharField(max_length = 255, blank = True, null = True)
    description = RichTextUploadingField(blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    #description2 = RichTextUploadingField(blank = True, null = True, config_name = 'special')
    #body = models.TextField(blank = True, null = True)
    #order = models.IntegerField(blank = True, null = True)
    #slug = models.SlugField(default = '', blank = True)


    def __str__(self):
        return '%s' % self.title


class comment(models.Model):
    content = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    camp = models.ForeignKey(Campaign, default=None, on_delete=models.CASCADE)
    def __str__(self):
        return self.content

    def check_comment(self):
        return '%s' % self.content


class reply(models.Model):
    content = models.TextField(max_length=1000)
    comment = models.ForeignKey(comment, default=None, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.date


class Backers(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    backer = models.CharField(max_length=50)
    email = models.EmailField(null = True)
    amount = models.FloatField(null=False, blank=False)
    token = models.CharField(max_length=120, null = True)
    date_backed = models.DateTimeField(default=timezone.now)
    def check_backer(self):
        return '%s' % self.backer
