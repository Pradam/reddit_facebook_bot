from random import choice
from django.db import models
from django.db.models.aggregates import Count

# Create your models here.

ACTIVE = ((0, 0), (2, 2))

OPTIONAL = {'null': True, 'blank': True}


class FacebookManager(models.Manager):
    def random(self):
        count = self.filter(active=2).values_list('id', flat=True)
        return choice(list(count))


class BaseContent(models.Model):
    createdOn = models.DateTimeField(auto_now_add=True)
    modifiedOn = models.DateTimeField(auto_now=True)
    active = models.IntegerField(choices=ACTIVE, default=2)

    class Meta:
        abstract = True


class Category(BaseContent):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.name)


class RedditSubscription(BaseContent):
    name = models.CharField(max_length=100)
    limit = models.IntegerField(default=10)
    link = models.TextField()

    def __str__(self):
        return '{} | {}'.format(self.name, self.link)


class PostLinks(BaseContent):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscribe = models.ForeignKey(RedditSubscription, on_delete=models.CASCADE)
    original_link = models.TextField()
    ups = models.IntegerField(default=0)
    objects = models.Manager()
    randoms = FacebookManager()

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.category.name,
                                          self.subscribe.name,
                                          self.original_link,
                                          self.ups)

    def switch(self):
        sw_dict = {2: 0, 0: 2}
        get_val = sw_dict.get(self.active)
        self.active = get_val
        self.save()


class FacebookPage(BaseContent):
    post = models.ForeignKey(PostLinks, on_delete=models.CASCADE)
    fb_id = models.TextField()

    def __str__(self):
        return '{} | {}'.format(self.post.original_link, self.fb_id)
