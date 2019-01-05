from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
#from marketplace.serializer import products_boughtSerializer #
from rest_framework.views import APIView
from .models import product, Order, OrderItem ,Transaction
from . import forms
from django.contrib import messages
from django.template.loader import render_to_string
import datetime
import stripe
from .extras import generate_order_id, transact, generate_client_token
from django.contrib import messages
#from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
from django import template
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail,EmailMessage

def test(request):
    product_blog = product.objects.all()
    return render(request, 'marketplace/test.html',{'products':product_blog})

def get_user_pending_order(request):
    # get order for the correct user
    order = Order.objects.filter(user=request.user, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0

def products_all(request):
    product_blog = product.objects.all()
    return render(request, 'marketplace/blog.html',{'products':product_blog})

def product_details(request, slug):
    pro_details = product.objects.get(pk=slug)
    return render(request, 'marketplace/product_details.html', {'details':pro_details})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def add_product(request):
    if request.method == "POST":
        form = forms.productform(request.POST,request.FILES)
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.fullname = request.user
            product_instance.save()
            return redirect('marketplace:products_blog')
    else:
        form = forms.productform()
        context={
        'form':form,
        'heading': "Add Product",
        }
    return render(request, 'marketplace/product_add.html',context)


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def my_products(request):
    uname = request.user
    my_product = product.objects.filter(fullname = uname)
    return render(request, 'marketplace/my_products.html',{'my_pro':my_product})


@login_required(login_url="http://127.0.0.1:8000/register/login/")
def edit_product(request, id = None):
    instance= get_object_or_404(product, pk= id)
    form= forms.productform(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('marketplace:products_blog')
    context={
        'form':form,
        'heading': "Edit Product",
    }
    return render(request, 'marketplace/product_add.html',context)

@login_required(login_url="http://127.0.0.1:8000/register/login/")
def delete_product(request, id):
    instance= get_object_or_404(product, pk= id)
    instance.delete()
    return redirect('marketplace:products_blog')
# django API
'''
class productsListView(APIView):
    def get(self,request):
        product_delivered = Transcation.objects.all()
        serializer = products_boughtSerializer(product_delivered,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = products_boughtSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
'''
def add_to_cart(request, id):
    if request.method == "POST":
        prod = product.objects.get(id=id)
        user_order, status = Order.objects.get_or_create(user=request.user, is_ordered=False)
        if status:
            ref_code = generate_order_id()
            order_item, status = OrderItem.objects.get_or_create(product=prod, ref_code=ref_code)
            user_order.items.add(order_item)
            user_order.ref_code = ref_code
            user_order.save()
            prod.quantity = int(prod.quantity) - int(1)
            prod.save()
        else:
            order_item, status = OrderItem.objects.get_or_create(product=prod, ref_code=user_order.ref_code)
            user_order.items.add(order_item)
            user_order.save()
            prod.quantity = int(prod.quantity) - int(1)
            prod.save()
        order_item.cost = order_item.qty * order_item.product.cost
        order_item.save()
        return render(request, 'marketplace/cart.html', {'order':user_order})
    else:
        prod = product.objects.get(id=id)
        user_order, status = Order.objects.get_or_create(user=request.user, is_ordered=False)
        order_item = OrderItem.objects.get(product=prod, ref_code=user_order.ref_code)
        order_item.cost = order_item.qty * order_item.product.cost
        order_item.save()
        return render(request, 'marketplace/blog.html', {'id':prod.pk})

def add_quantity(request, id):
    item = OrderItem.objects.get(pk=id)
    if item.qty < item.product.quantity:
        item.qty = item.qty + 1
        item.save()
    return redirect('/marketplace/add_to_cart/'+str(item.product.id))

def remove_quantity(request, id):
    item = OrderItem.objects.get(pk=id)
    item.qty = item.qty - 1
    item.save()
    return redirect('/marketplace/add_to_cart/'+str(item.product.id))

def delete(request, id):
    item = OrderItem.objects.get(pk=id)
    item.delete()
    return redirect('marketplace:products_blog')

def add_tocart(request):
    return render(request, 'marketplace/cart.html')

@login_required()
def checkout(request, **kwargs):
    client_token = generate_client_token()
    existing_order = get_user_pending_order(request)
    amt = int(existing_order.get_cart_total())
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        amt = int(existing_order.get_cart_total())
        if token:
            # STRIPE
            try:
                charge = stripe.Charge.create(
                    amount= amt,
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

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
            # BRAINTREE PAYPAL
            result = transact({
                'amount': amt,
                'payment_method_nonce': request.POST['payment_method_nonce'],
                'options': {
                    "submit_for_settlement": True
                }
            })

            if result.is_success or result.transaction:
                entry_token =result.transaction.id
                existing_order = get_user_pending_order(request)
                # update the placed order
                existing_order.is_ordered=True
                existing_order.date_ordered=datetime.datetime.now()
                existing_order.save()
                order_items = existing_order.items.all()
                order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
                # create a transaction
                transaction = Transaction(user=request.user,
                                        token=entry_token,
                                        order_id=existing_order.id,
                                        amount=existing_order.get_cart_total(),
                                        success=True)
                transaction.save()

                ## mail notification as funds receivd to the project #
                User = get_user_model()
                uname = request.user.username
                Funds = existing_order.get_cart_total()
                order_id = existing_order.id
                mail_id = User.objects.get(username = uname).email

                subject = "Recived Funds"
                to = ['ruthala.shiva512@gmail.com',]
                to.append(mail_id)
                from_email = 'ruthala.shiva512@gmail.com'

                details = {
                    'donar': uname,
                    'amount': Funds,
                    'project': order_id,
                }

                message = get_template('startFundraiser/mail.html').render(dict(details))
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()

                messages.info(request, "Thank you! Your purchase was successful!")
                return HttpResponse("Thank you! Your purchase was successful!")
            else:
                for x in result.errors.deep_errors:
                    messages.info(request, x)
                return redirect(reverse('startFundraiser:checkout'))

    context = {
        'order': amt,
        'client_token': client_token,
        'STRIPE_PUBLISHABLE_KEY': publishKey
    }

    return render(request, 'startFundraiser/checkout.html', context)
