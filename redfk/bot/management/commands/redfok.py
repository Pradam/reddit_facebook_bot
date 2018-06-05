import datetime
import requests
from random import choice
from django.core.management.base import BaseCommand
from django.core.management import call_command
from redfk.settings import (access_token)
from bot.views import (ImportRedditPost,)
from bot.models import (PostLinks, FacebookPage, StackOverflow)


class Durations(object):

    @classmethod
    def get_current_month(cls):
        today = datetime.datetime.now().date()
        month = today.month
        return month


class Command(BaseCommand):
    help = 'Posting Reddit Link to Facebook Page.'

    def handle(self, *args, **options):
        instance_reddit = ImportRedditPost()
        month = Durations.get_current_month()
        get_last_site = FacebookPage.objects.latest().get_switch()
        if get_last_site == 0:
            rand_post = PostLinks.randoms.filter(active=2, createdOn__month=month)
            if rand_post:
                post = rand_post[0]
                data = requests.post("https://graph.facebook.com/v3.0/feed?link=%s&access_token=%s" % (post.original_link,access_token))
                FacebookPage.objects.create(site=0, post=post, fb_id=data.text)
                post.switch()
                print(data.text)
            else:
                instance_reddit.save_link()
                call_command('redfok')
        else:
            st_ids = list(StackOverflow.objects.filter(active=2).values_list('id', flat=True))
            if st_ids:
                get_stack_obj = StackOverflow.objects.get(id=choice(st_ids))
                data = requests.post("https://graph.facebook.com/v3.0/feed?link=%s&access_token=%s" % (get_stack_obj.link,access_token))
                FacebookPage.objects.create(site=1, stack=get_stack_obj, fb_id=data.text)
                get_stack_obj.active = 0
                get_stack_obj.save()
                print(data.text)
            else:
                rand_post = PostLinks.randoms.filter(active=2, createdOn__month=month)
                if rand_post:
                    post = rand_post[0]
                    data = requests.post("https://graph.facebook.com/v3.0/feed?link=%s&access_token=%s" % (post.original_link,access_token))
                    FacebookPage.objects.create(site=0, post=post, fb_id=data.text)
                    post.switch()
                    print(data.text)
                else:
                    instance_reddit.save_link()
                    call_command('redfok')
