import datetime
import requests
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from redfk.settings import (access_token)
from bot.views import (ImportRedditPost,)
from bot.models import (PostLinks, FacebookPage)


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
        rand_post = PostLinks.randoms.all()
        if rand_post:
            post = rand_post[0]
            if post.createdOn.month == month:
                data = requests.post("https://graph.facebook.com/v3.0/feed?link=%s&access_token=%s" % (post.original_link,access_token))
                FacebookPage.objects.create(post=post, fb_id=data.text)
                post.switch()
                send_mail('Facebook Post Status',
                          data.text,
                          'doddapypers@python.org',
                          ['pradamabhilash@gmail.com'],
                          fail_silently=False,)
            else:
                PostLinks.objects.filter(active=2).delete()
                instance_reddit.save_link()
        else:
            instance_reddit.save_link()
