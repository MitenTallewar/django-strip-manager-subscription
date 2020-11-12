from django.urls import path

from .views import SubscriptionListView, SubscriptionDetailView, \
  SubscriptionChargeView,StripeAuthorizeView,\
  CancelSubscriptions, SignUp,ResumeSubscriptions,StripeAuthorizeCallbackView


urlpatterns = [
  path('', SubscriptionListView.as_view(), name='subscription_list'),
  path('subscriptions/charge/', SubscriptionChargeView.as_view(), name='charge'),
  path('subscriptions/cancel/',CancelSubscriptions.as_view(), name='subscription_cancel'),
  path('subscriptions/resume/',ResumeSubscriptions.as_view(), name='subscription_resume'),
  path('<slug:slug>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
  path('authorize/', StripeAuthorizeView.as_view(), name='authorize'),
  path('oauth/callback/', StripeAuthorizeCallbackView.as_view(), name='authorize_callback'),
]
