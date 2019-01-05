import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from PIL import Image
from django.core.files import File
from .forms import CampaignForm, FaqsForm
from django.contrib.auth.models import User
from .models import Campaign, Faqs, comment, Reward, Backers, RewardClaimed


class CampaignModelTest(TestCase):

    def test_string_representation(self):
        campaign = Campaign(campaign_Title="My campaign title")
        self.assertEqual(str(campaign), campaign.campaign_Title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Campaign._meta.verbose_name_plural), "campaigns")


class Modeltest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='tanviagarwal', password='icebreaker')
        campaign = Campaign.objects.create(
            user=user,
            campaign_Title="My campaign title",
            campaign_Tagline="My campaign tagline",
            campaign_Category='comics',
            city='Chennai',
            overview="Overview",
            image="https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiTlY2u-JjfAhXZWisKHTnKCT8QjRx6BAgBEAU&url=https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2FFile%3AGold_Star.svg&psig=AOvVaw0JI7KK1S6TJd9tHMnhExIc&ust=1544657665045761",
            goal=10000.00,
            end_Date=(datetime.date.today() + datetime.timedelta(weeks=2)),
            start_Date=datetime.date.today(),
        )
        Faqs.objects.create(campaign=campaign)
        reward = Reward.objects.create(campaign=campaign, amount=1000.00, perks='Thank-you Cards')
        RewardClaimed.objects.create(user=user, reward=reward)
        Backers.objects.create(backer='Tanvi', campaign=campaign, amount=1000.00)
        comment.objects.create(content='Hey', camp=campaign, author=user)

    def test_faq(self):
        faq = Faqs.objects.get(id=1)
        self.assertEquals(faq.check_faq(), "What are you raising funds for?")

    def test_comment(self):
        comments = comment.objects.get(id=1)
        self.assertEquals(comments.check_comment(), "Hey")

    def test_reward(self):
        reward = Reward.objects.get(id=1)
        self.assertEquals(reward.check_reward(), "Thank-you Cards")

    def test_backers(self):
        backer = Backers.objects.get(id=1)
        self.assertEquals(backer.check_backer(), "Tanvi")

    def test_rewardclaimed(self):
        claimed = RewardClaimed.objects.get(id=1)
        self.assertEquals(claimed.check_rewardclaimed(), "My campaign title")
