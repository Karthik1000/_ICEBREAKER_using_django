from django.test import TestCase

from .models import GroupTable, MemberTable, CommentTable, UpdateTable
from django.contrib.auth.models import User
from django.urls import reverse

class modeltest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # my on setup
        user = User.objects.create(username='saurabh', password='admin1234')
        group = GroupTable.objects.create(title = 'party', founder=user)
        CommentTable.objects.create(comment='my comment', group=group, user=user)

    def test_group(self):
        group = GroupTable.objects.get(id = 1)
        self.assertEquals(group.checkinggroup(),"party")

    def test_comment(self):
        comment = CommentTable.objects.get(id = 1)
        self.assertEquals(comment.checkingcomment(),"party")


class TestUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='saurabh', first_name='saurabh', last_name='petkar',
                                   email='saurabh@gmail.com', password='saurabh')
        #state : group
        #city: comment
        #address: update

        group = GroupTable.objects.create(title = 'party', founder=user)
        comment = CommentTable.objects.create(comment='my comment', group=group, user=user)
        update = UpdateTable.objects.create(update='my update', group=group)

    def test_user(self):
        update = UpdateTable.objects.get(id = 1)
        self.assertEquals(update.checkingupdate(),"my update")

    def test_maxlength(self):
        update = UpdateTable.objects.get(id = 1)
        max_len = update._meta.get_field('update').max_length
        self.assertEquals(max_len,1000)



from django.test.client import Client

class UsersListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user(username='john',
        email='lennon@thebeatles.com', password='johnpassword')

    # def test_view_uses_correct_template_index(self):
    #     response = self.client.get(reverse('community:view_group'))
    #     self.assertEqual(response.status_code, 302)
        #redirected, cuz user is not logged in
        #self.assertTemplateUsed(response, 'community/view-community.html')

        #do for all the functions


        #url testing

    def test_view_url_accessible_by_name_index(self):
        response = self.client.get(reverse('community:view_group'))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_makegroup(self):
        response = self.client.get(reverse('community:make_group'))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name_mygroup(self):
        response = self.client.get(reverse('community:my_group'))
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name_joinedgroup(self):
        response = self.client.get(reverse('community:joined_group'))
        self.assertEqual(response.status_code, 302)


    def test_profile_list_usersnotloggedin_profile_list(self):
        response = self.client.get(reverse('community:profile_list'))
        self.assertEqual(response.status_code, 302)

    def test_view_url_user_logged_in_view_group(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('community:view_group'))
        self.assertTemplateUsed(response, 'community/view-community.html')
        self.assertEqual(response.status_code, 200)

    def test_view_url_user_logged_in_make_group(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('community:make_group'))
        self.assertTemplateUsed(response, 'community/make-group.html')
        self.assertEqual(response.status_code, 200)

    def test_view_url_user_logged_in_my_group(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('community:my_group'))
        self.assertTemplateUsed(response, 'community/my-group.html')
        self.assertEqual(response.status_code, 200)

    def test_view_url_user_logged_in_joined_group(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('community:joined_group'))
        self.assertTemplateUsed(response, 'community/joined-group.html')
        self.assertEqual(response.status_code, 200)

    def test_view_url_user_logged_in_profile_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('community:profile_list'))
        self.assertTemplateUsed(response, 'community/all-profiles.html')
        self.assertEqual(response.status_code, 200)








