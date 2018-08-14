from .models import Tweet, ReTweet
from user.serializers import UserSerializer
from rest_framework import serializers


class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ("id", "content", "user", "date_add")


class ReTweetSerializer(serializers.ModelSerializer):
    re_tweet = TweetSerializer()

    class Meta:
        model = ReTweet
        fields = ("id", "re_tweet", "date_add")
