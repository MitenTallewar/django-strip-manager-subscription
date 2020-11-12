from django.contrib import admin

from .models import Subscription,CustomUser

class SubscriptionAdmin(admin.ModelAdmin):
    pass

class CustomuserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(CustomUser,CustomuserAdmin)