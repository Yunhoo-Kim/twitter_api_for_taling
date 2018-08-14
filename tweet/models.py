from django.db import models
from user.models import TwitterUser


class Tweet(models.Model):
    user = models.ForeignKey(TwitterUser, related_name="tweet", on_delete=models.CASCADE)
    content = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tweet"


class ReTweet(models.Model):
    tweet = models.ForeignKey(Tweet, related_name="re_tweet", on_delete=models.CASCADE)
    user = models.ForeignKey(TwitterUser, related_name="re_tweet", on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "retweet"

