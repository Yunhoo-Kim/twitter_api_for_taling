from .models import Tweet, ReTweet
from user.serializers import UserSerializer, User
from rest_framework import serializers


class TweetSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ("id", "content", "user", "date_add", "user_name")

    def get_user_name(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)


class ReTweetSerializer(serializers.ModelSerializer):
    re_tweet = TweetSerializer()

    class Meta:
        model = ReTweet
        fields = ("id", "re_tweet", "date_add")


class UserPageSerializer(serializers.ModelSerializer):
    tweet = TweetSerializer(many=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "tweet")
