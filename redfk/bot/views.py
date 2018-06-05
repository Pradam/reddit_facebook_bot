import requests
import praw
from redfk.settings import (cliend_id,
                            client_secret,
                            username,
                            password,
                            user_agent)
from .models import (RedditSubscription,
                     Category,
                     PostLinks, StackOverflow)
# Create your views here.

stack_overflow_lik = "https://api.stackexchange.com/docs/questions#order=desc&sort=month&tagged=python&filter=default&site=stackoverflow&run=true"


class ImportRedditPost:

    def __init__(self):
        self.kwargs = {'limit': 15}
        self.reddit = praw.Reddit(client_id=cliend_id,
                                  client_secret=client_secret,
                                  password=password,
                                  user_agent=user_agent,
                                  username=username)

    def check_url(self, instance):
        url = instance.url
        split = url.rsplit('.', 1)
        if len(split) == 2:
            if split[1] in ['png', 'jpeg', 'jpg', 'svg', 'tiff', 'gif', 'bmp']:
                url = instance.shortlink
        return url

    def save_link(self):
        redsub = RedditSubscription.objects.filter(active=2).values_list('id', flat=True)
        get_redsub_name = lambda x: RedditSubscription.objects.get(active=2, id=x).name
        instance_subit = [(_id, self.reddit.subreddit(get_redsub_name(_id)))
                          for _id in redsub]
        cat = Category.objects.filter(active=2).values_list('id', flat=True)
        for instance_id, instance in instance_subit:
            for sort in cat:
                sort_name = Category.objects.get(id=sort)
                praw_list = getattr(instance, sort_name.name)(**self.kwargs)
                for submission in praw_list:
                    link = self.check_url(submission)
                    PostLinks.objects.create(category_id=sort,
                                             subscribe_id=instance_id,
                                             original_link=link,
                                             ups=submission.ups)

    def save_stack(self):
        url = "https://api.stackexchange.com/2.2/questions?order=desc&sort=votes&tagged=python&site=stackoverflow&pagesize=100"
        stack_overflow = requests.get(url)
        stack_response = stack_overflow.json()
        json_value = stack_response.get('items', [])
        if json_value:
            for val in json_value:
                link, score = val.get('link'), val.get('score')
                StackOverflow.objects.create(link=link, score=score)
