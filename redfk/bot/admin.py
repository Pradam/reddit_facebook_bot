from django.contrib import admin

from .models import (Category, RedditSubscription, PostLinks, FacebookPage, StackOverflow)
# Register your models here.

admin.site.register([Category, RedditSubscription, PostLinks, FacebookPage, StackOverflow])
