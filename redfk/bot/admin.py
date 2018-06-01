from django.contrib import admin

from .models import (Category, RedditSubscription, PostLinks, FacebookPage)
# Register your models here.

admin.site.register([Category, RedditSubscription, PostLinks, FacebookPage])
