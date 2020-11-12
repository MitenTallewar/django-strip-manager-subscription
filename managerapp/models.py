from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .managers import UserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), unique=True)
    firstname = models.CharField('firstname', max_length=50)
    lastname = models.CharField('lastname', max_length=50)
    dob = models.DateField('dob')
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    address= models.CharField('address',max_length=50)
    company = models.CharField('company', max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    stripe_user_id = models.CharField(max_length=255, blank=True)
    stripe_access_token = models.CharField(max_length=255, blank=True)
    subscription = models.ForeignKey("Subscription",on_delete=models.CASCADE)
    is_subscription_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Subscription(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
