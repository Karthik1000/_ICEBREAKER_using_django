from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.db.models import Q, F
from datetime import date, datetime, timedelta
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views import generic
from .models import Campaign, Faqs, Update, Post, comment, reply, Reward, RewardClaimed
from .forms import CampaignForm, UserForm, UpdateForm, FaqsForm, PostForm, createcomment, createreply, BackersForm, \
    RewardModelFormset
from django.contrib.auth import get_user_model
import re
# django-rest API
from rest_framework import status
from .models import Backers  ##API models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import fundsSerializer
from rest_framework.views import APIView

from .extras import generate_order_id, transact, generate_client_token  # payment
from django.contrib import messages
# from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
from django import template
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def campaign_status():
    Campaign.objects.filter(start_Date__lte=date.today(), end_Date__gte=date.today()).update(campaign_status='started')
    Campaign.objects.filter(start_Date__lte=date.today(), end_Date__lte=date.today(), goal__lte=F('pledged')).update(
        campaign_status='successfully')
    Campaign.objects.filter(start_Date__lte=date.today(), end_Date__lte=date.today(), goal__gte=F('pledged')).update(
        campaign_status='unsuccessfully')


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_update(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.campaign = campaign
            update.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    else:
        form = UpdateForm()
    return render(request, 'startFundraiser/add_update.html', {'form': form})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_rewards(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    template_name = 'startFundraiser/rewards.html'
    heading_message = 'Rewards'
    if request.method == 'POST':
        formset = RewardModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                reward = form.save(commit=False)
                print(form.cleaned_data)
                reward.campaign = campaign
                reward.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    else:
        formset = RewardModelFormset(queryset=Reward.objects.none())
        return render(request, template_name, {
            'formset': formset,
            'heading': heading_message,
        })


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def claim_reward(request, pk):
    reward = get_object_or_404(Reward, pk=pk)
    campaign = reward.campaign
    campaign.pledged = campaign.pledged + reward.amount
    reward.claimed = reward.claimed + 1
    campaign.save()
    reward.save()
    return render(request, 'startFundraiser/claim_reward.html', {'reward': reward})


def campaign_support(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    print(campaign)
    if request.method == "POST":
        form = BackersForm(request.POST)
        if form.is_valid():
            print('valid')
            backers = form.save(commit=False)
            backers.campaign = campaign
            backers.amount = form.cleaned_data['amount']
            if backers.amount < 50:
                context = {
                    'error_message': 'Please donate an amount greater than or equal to 50',
                    'form': form,
                }
                return render(request, 'startFundraiser/support_it.html', context)
            backers.save()
            campaign.pledged = campaign.pledged + backers.amount
            campaign.people_pledged = campaign.people_pledged + 1
            campaign.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    return render(request, 'startFundraiser/support_it.html', {'form': BackersForm(request.POST)})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_comment(request, pk):
    campaign1 = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        form = createcomment(request.POST)
        if form.is_valid():
            a = request.POST.get('content')
            regex = re.compile('[^a-zA-Z]')
            e = regex.sub('', a)
            b = ['crap', 'shit']
            d = 0
            for c in b:
                if (e.find(c) != -1):
                    d = d + 1
            if d == 0:
                content = request.POST.get('content')
                comment1 = comment.objects.create(camp=campaign1, author=request.user, content=content)
                comment1.save()
                return redirect('startFundraiser:campaign_detail', campaign_id=pk)
                # return redirect("{% url 'startFundraiser:campaign_detail' campaign_id = campaign1.pk %}")
            else:
                return HttpResponse('Do not use bad words')
    else:
        form = createcomment()
    return render(request, 'startFundraiser/createcomment.html', {'form': form})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_faq(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    print(campaign)
    if request.method == "POST":
        form = FaqsForm(request.POST)
        if form.is_valid():
            print("valid")
            faq = form.save(commit=False)
            faq.campaign = campaign
            faq.save()
            return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    else:
        form = FaqsForm()
    return render(request, 'startFundraiser/add_faq.html', {'form': form, 'campaign': campaign})


def index(request):
    projects = Campaign.objects.all()
    query = request.GET.get('q')
    if query:
        projects = projects.filter(
            Q(campaign_Title__icontains=query) |
            Q(campaign_Tagline__icontains=query) |
            Q(campaign_Category__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})
    else:
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})



def home(request):
    campaign_status()
    camp_count = Campaign.objects.count()
    if camp_count >= 3:
        most_liked = Campaign.objects.order_by('-likes', '-pledged')[0:3]
        return render(request, 'startFundraiser/home.html', {'most_liked': most_liked, 'camp_count': camp_count})
    return render(request, 'startFundraiser/home.html')


def creative(request):
    projects = Campaign.objects.filter(campaign_Category__icontains='art')
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def social(request):
    projects = Campaign.objects.filter(campaign_Category__icontains='culture')
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def tech(request):
    projects = Campaign.objects.filter(campaign_Category__icontains='education')
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def campaigns(request):
    projects = Campaign.objects.all()
    return render(request, 'startFundraiser/campaigns.html', {'projects': projects})


def validate_start_campaign(start, end, file_type):
    error_message = {}
    duration = end - start
    delta = int(duration.days)
    print(delta)
    if delta > 40 or delta < 7:
        error_message['duration'] = 'Check the campaign duration'
    if file_type not in IMAGE_FILE_TYPES and file_type != 'empty':
        error_message['image']: 'Image file must be PNG, JPG, or JPEG'

    return error_message


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def start_campaign(request):
    form = CampaignForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        campaign = form.save(commit=False)
        campaign.user = request.user
        file_type = 'empty'
        if campaign.image:
            campaign.image = request.FILES['image']
            file_type = campaign.image.url.split('.')[-1]
            file_type = file_type.lower()
        start = form.cleaned_data['start_Date']
        end = form.cleaned_data['end_Date']
        error_message = validate_start_campaign(start, end, file_type)
        print(error_message)
        if error_message:
            context = {
                'campaign': campaign,
                'form': form,
                'error_message': error_message,
            }
            return render(request, 'startFundraiser/campaign-form.html', context)
        campaign.save()
        return render(request, 'startFundraiser/detail.html', {'campaign1': campaign})
    context = {
        "form": form,
    }
    return render(request, 'startFundraiser/campaign-form.html', context)


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def campaign_edit(request, pk, template_name='startFundraiser/campaign-editform.html'):
    campaign = get_object_or_404(Campaign, pk=pk)
    form = CampaignForm(request.POST or None, instance=campaign)
    if form.is_valid() and request.user == campaign.user:
        form.save()
        return redirect('startFundraiser:campaign_detail', campaign_id=pk)
    return render(request, template_name, {'form': form})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def campaign_delete(request, pk, template_name='startFundraiser/campaign-deleteform.html'):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST' and request.user == campaign.user and campaign.pledged == 0:
        campaign.delete()
        return redirect('startFundraiser:campaigns')
    return render(request, template_name, {'object': campaign})


def detail(request, campaign_id):
    campaign1 = get_object_or_404(Campaign, pk=campaign_id)
    is_liked = False
    if campaign1.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.user.is_authenticated and campaign1.user == request.user:
        if campaign1.tags:
            tag = campaign1.tags.split()
            context = {
                'is_editable': True,
                'campaign1': campaign1,
                'tag': tag,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
        else:
            context = {
                'is_editable': True,
                'campaign1': campaign1,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
    else:
        if campaign1.tags:
            tag = campaign1.tags.split()
            context = {
                'campaign1': campaign1,
                'tag': tag,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
        else:
            context = {
                'campaign1': campaign1,
                'is_liked': is_liked,
                'total_likes': campaign1.total_likes()
            }
    return render(request, 'startFundraiser/detail.html', context)


def blog_post(request):
    web_updates = Post.objects.all()
    return render(request, 'startFundraiser/view_post.html', {'posts': web_updates})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_post(request):
    if request.user.groups.filter(name ='admin').exists():
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post_item = form.save(commit =False)
                post_item.save()
                return redirect('http://127.0.0.1:8000/')
                #return HttpResponse("Saved post")
        else:
            form = PostForm()
        return render(request, 'startFundraiser/post.html',{'form':form})
    else:
        return HttpResponse("Sorry..., You have no previlage")
@login_required
def edit_post(request, id= None):
    if request.user.groups.filter(name ='admin').exists():
        instance= get_object_or_404(Post, pk= id)
        form= PostForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000/')
        context={
            'form':form,
        }
        return render(request, 'startFundraiser/post.html', context)
    else:
        return HttpResponse("Sorry..., You have no previlage")
@login_required
def del_post(request, id ):
    if request.user.groups.filter(name ='admin').exists():
        instance= get_object_or_404(Post, pk= id)
        instance.delete()
        return redirect('http://127.0.0.1:8000/')
    else:
        return HttpResponse("Sorry..., You have no previlage")


def like_camp(request):
    campaign = get_object_or_404(Campaign, id=request.POST.get('id'))
    is_liked = False
    if campaign.likes.filter(id=request.user.id).exists():
        is_liked = False
        campaign.likes.remove(request.user)
    else:
        is_liked = True
        campaign.likes.add(request.user)
    context = {
        'campaign': campaign,
        'is_liked': is_liked,
        'total_likes': campaign.total_likes()
    }

    if request.is_ajax():
        html = render_to_string('startFundraiser/like_section.html', context, request=request)
    return JsonResponse({'form': html})


def page_not_found(request):
    return render(request, 'startFundraiser/nopage.html')


def index(request):
    projects = Campaign.objects.all()
    query = request.GET.get('q')
    if query:
        projects = projects.filter(
            Q(campaign_Title__icontains=query) |
            Q(campaign_Tagline__icontains=query) |
            Q(campaign_Category__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})
    else:
        return render(request, 'startFundraiser/campaigns.html', {'projects': projects})

# payment
def pay(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    context={
    'pk':pk,

        }
    return render(request, 'startFundraiser/support_it.html', context)
@login_required()
def checkout1(request, id, **kwargs):
    reward = get_object_or_404(Reward, pk=id)
    client_token = generate_client_token()
    publishKey = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=int(reward.amount),
                    currency='usd',
                    description='Example charge',
                    source=token,
                )
                print(amt)
                return redirect(reverse('startFundraiser:update_records',
                        kwargs={
                            'token': token,
                            'pk':pk,
                            'amount':amt,
                        })
                    )
            except stripe.CardError as e:
                message.info(request, "Your card has been declined.")
        else:
            result = transact({
                'amount': int(reward.amount),
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                entry_token =result.transaction.id
                reward = get_object_or_404(Reward, pk=id)

                # create a transaction record
                transaction = RewardClaimed(user=request.user,
                                            reward=reward,
                                        )
                transaction.save()
                reward.claimed = int(reward.claimed) + int(1)
                reward.save()

                ## mail notification as funds receivd to the project #

                messages.info(request, "Thank you! Your purchase was successful!")
                #return HttpResponse("updated")
                #testing
                #return render(request, 'acknowledgement.html', details)
                return redirect("http://127.0.0.1:8000/")

                #return redirect(reverse('startFundraiser:update_records',pk))
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('startFundraiser:checkout'+str(pk)))

    context = {
        'order': int(reward.amount),
        'client_token': client_token,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'startFundraiser/checkout.html', context)




@login_required()
def checkout(request, pk, **kwargs):
    campaign = get_object_or_404(Campaign, pk=pk)
    client_token = generate_client_token()
    publishKey = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        if 'pay' in request.POST:
            global amt
            amt = request.POST['pay']
            global backer
            backer = request.POST['backer']
            print(amt)
        else:
            token = request.POST.get('stripeToken', False)
            if token:
                try:
                    charge = stripe.Charge.create(
                        amount=amt,
                        currency='usd',
                        description='Example charge',
                        source=token,
                    )
                    print(amt)
                    return redirect(reverse('startFundraiser:update_records',
                            kwargs={
                                'token': token,
                                'pk':pk,
                                'amount':amt,
                            })
                        )
                except stripe.CardError as e:
                    message.info(request, "Your card has been declined.")
            else:
                result = transact({
                    'amount': amt,
                    'payment_method_nonce': request.POST['payment_method_nonce'],
                    'options': {
                        "submit_for_settlement": True
                    }
                })

                if result.is_success or result.transaction:
                    entry_token =result.transaction.id
                    '''
                    return redirect(reverse('startFundraiser:update_records',
                            kwargs={
                                'token': result.transaction.id,
                                'pk':pk,
                                'amount':amt,
                            })
                        )
                    '''
                    campaign = get_object_or_404(Campaign, pk=pk)

                    # create a transaction record
                    transaction = Backers(backer=request.user,
                                            campaign = campaign,
                                            email = request.user.email,
                                            token=entry_token ,
                                            amount = amt,
                                            )
                    transaction.save()
                    campaign.pledged = float(campaign.pledged) + float(amt)
                    campaign.people_pledged = campaign.people_pledged + 1
                    campaign.save()

                    ## mail notification as funds receivd to the project #
                    User = get_user_model()
                    uname = request.user.username
                    Funds =  amt
                    project = campaign.campaign_Title
                    Project_by = campaign.user
                    mail_id = User.objects.get(username = Project_by).email

                    subject = "Recived Funds"
                    to = ['ruthala.shiva512@gmail.com',]
                    to.append(mail_id)
                    from_email = 'ruthala.shiva512@gmail.com'

                    details = {
                        'donar': uname,
                        'amount': Funds,
                        'reciver': Project_by,
                        'project': project,
                    }

                    message = get_template('startFundraiser/mail.html').render(dict(details))
                    msg = EmailMessage(subject, message, to=to, from_email=from_email)
                    msg.content_subtype = 'html'
                    msg.send()

                    messages.info(request, "Thank you! Your purchase was successful!")
                    #return HttpResponse("updated")
                    #testing
                    #return render(request, 'acknowledgement.html', details)
                    return HttpResponse("Thank you! Your purchase was successful!")

                    #return redirect(reverse('startFundraiser:update_records',pk))
                else:
                    for x in result.errors.deep_errors:
                        messages.info(request, x)
                    return redirect(reverse('startFundraiser:checkout'+str(pk)))

        context = {
            'order': amt,
            'client_token': client_token,
            'STRIPE_PUBLISHABLE_KEY': publishKey
        }

        return render(request, 'startFundraiser/checkout.html', context)




@login_required()
def update_transaction_records(request,pk):
    campaign = get_object_or_404(Campaign, pk=pk)

    # create a transaction
    transaction = Backers(backer=request.user,
                            campaign = campaign,
                            email = request.user.email,
                            token=entry_token ,
                            amount = amt,
                            )
    # save the transcation (otherwise doesn't exist)
    transaction.save()
    campaign.pledged = float(campaign.pledged) + float(amt)
    campaign.people_pledged = campaign.people_pledged + 1
    campaign.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return HttpResponse("updated")
    #return redirect(reverse('accounts:my_profile'))

# django API
class fundsListView(APIView):
    def get(self, request):
        fundings = Backers.objects.all()
        serializer = fundsSerializer(fundings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = fundsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
