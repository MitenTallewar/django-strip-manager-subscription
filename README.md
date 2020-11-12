## Clone project from git
     https://github.com/MitenTallewar/django-strip-manager-subscription.git
## Install dependencies with following command
     pip install -r requirements.txt
## Migrate (please check database section in settings.py)
    manage.py migrate
## Create testing account on stripe and add publishable keys and secret key in settings.py 
  STRIPE_PUBLISHABLE_KEY = '< your stripe publishable key >'\
  STRIPE_SECRET_KEY = '< your stripe secrest key >'\
  STRIPE_CONNECT_CLIENT_ID = '< your Stripe clinet id>'  
## Run project 
   manage.py runserver
## URL
   http://localhost:8000
## Register manager
   http://localhost:8000/register
## Login to the sytem using email and password
   http://localhost:8000
   
### Purchase Subscription following by providing credit card details. Note. for testing creditcard details will be present on payment page.   

### Verify success message. and go to home page to see your subscription

### Logout and Login to application again. this time we will be to see active subscription

### To cancel subscription, just click on link to cancel subscription on home page after login.
