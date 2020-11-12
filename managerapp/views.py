import json
import urllib
import stripe
import requests
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Subscription,CustomUser


class SubscriptionListView(ListView):
    model = Subscription
    template_name = 'subscriptions/subscription_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SubscriptionListView, self).get_context_data(*args, **kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(SubscriptionListView, self).render_to_response(context, **response_kwargs)


class SubscriptionDetailView(DetailView):
    model = Subscription
    template_name = 'subscriptions/subscription_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SubscriptionDetailView, self).get_context_data(*args, **kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

    def render_to_response(self, context, **response_kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return super(SubscriptionDetailView, self).render_to_response(context, **response_kwargs)


class SubscriptionChargeView(View):

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        json_data = json.loads(request.body)
        subscription_id = Subscription.objects.filter(id=json_data['subscription_id']).first()
        print("Subscription--",subscription_id)
        user_id = json_data['user']
        try:
            customer = get_or_create_customer(
                self.request.user.email,
                json_data['token'],
            )
            subscription_amount = json_data['amount']
            try:
                charge = stripe.Charge.create(
                    amount=subscription_amount,
                    currency='inr',
                    customer=customer.id,
                    description=json_data['description']
                )
            except Exception as e:
                print('Error while charge create is:', e)

            if charge:
                # update user with subscription
                customUser = CustomUser.objects.get(id = user_id)
                print('Retrieved user for id= ', customUser)
                customUser.subscription = subscription_id
                customUser.is_subscription_active = True
                customUser.save(update_fields=['subscription','is_subscription_active'])
                return JsonResponse({
                    'status': 'success'
                    }, status=202)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'}, status=500)

# helpers

def get_or_create_customer(email, token):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Customer.create(
        email=email,
        source=token,
    )


class StripeAuthorizeView(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        url = 'https://connect.stripe.com/oauth/authorize'
        params = {
            'response_type': 'code',
            'scope': 'read_write',
            'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
            'redirect_uri': f'http://localhost:8000/users/oauth/callback'
        }
        url = f'{url}?{urllib.parse.urlencode(params)}'
        return redirect(url)


class StripeAuthorizeCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        if code:
            data = {
                'client_secret': settings.STRIPE_SECRET_KEY,
                'grant_type': 'authorization_code',
                'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
                'code': code
            }
            url = 'https://connect.stripe.com/oauth/token'
            resp = requests.post(url, params=data)
            print(resp.json())
            # add stripe info to the seller
            stripe_user_id = resp.json()['stripe_user_id']
            stripe_access_token = resp.json()['access_token']
            seller = CustomUser.objects.filter(user_id=self.request.user.id).first()
            seller.stripe_access_token = stripe_access_token
            seller.stripe_user_id = stripe_user_id
            seller.save()
        url = reverse('home')
        response = redirect(url)
        return response

class CancelSubscriptions(View):

    def patch(self, request):
        json_data = json.loads(request.body)
        user_id = json_data['user']
        print('userid=',user_id)
        customUser = CustomUser.objects.get(id = user_id)
        customUser.is_subscription_active = False
        customUser.save(update_fields=['is_subscription_active'])
        return render(request,'home.html')



class ResumeSubscriptions(View):

    def patch(self, request):
        json_data = json.loads(request.body)
        user_id = json_data['user']
        print('userid=',user_id)
        customUser = CustomUser.objects.get(id = user_id)
        customUser.is_subscription_active = True
        customUser.save(update_fields=['is_subscription_active'])
        return render(request,'home.html')


class RegisterUser(View):
    def post(self,request):
        data = request.POST
        user = CustomUser.objects.create_user(data['email'], data['password'])
        user.firstname=data['firstname']
        user.lastname=data['lastname']
        user.address=data['address']
        user.company=data['company']
        user.dob=data['dob']
        user.is_staff =True
        user.save()
        msg ='You are registered successfully...!'
        return render(request,'login.html',{"msg":msg})


class SignUp(View):
    def get(self,request):
        return render(request,'register.html')


def email_verify(request):
    json_data = json.loads(request.body)
    email = json_data['email']
    cust = CustomUser.objects.filter(email=email).first()
    if cust:
        return JsonResponse({'msg': True})
    else:
        return JsonResponse({'msg': False})