from rest_framework.views import APIView
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from .serializers import TweetSerializer, Tweet
from user.models import TwitterUser
from helper.authentications import CustomJWTTokenAuthentication
from helper.makejson import MakeJSON


class TweetView(JSONWebTokenAPIView):
    """
    post: Write Tweet
    """
    authentication_classes = (CustomJWTTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    serializer_class = TweetSerializer

    def __init__(self):
        self.makejson = MakeJSON()

    def post(self, request, *args, **kwargs):
        query = request.data
        query["user"] = request.user.id
        ser = TweetSerializer(data=query)

        if not ser.is_valid():
            return self.makejson.get400ResponseWithResponse()

        ser.save()
        return self.makejson.getResponse()


class UserTweetListView(APIView):
    """
    get: Get User Tweet list by user id
    """
    authentication_classes = (CustomJWTTokenAuthentication, )
    permission_classes = (permissions.AllowAny, )
    renderer_classes = (JSONRenderer, )

    def __init__(self):
        self.makejson = MakeJSON()

    def get(self, request, id):

        user = TwitterUser.objects.get(id=id)

        data = TweetSerializer(user.tweet.all(), many=True).data
        self.makejson.addResult(tweets=data)

        return self.makejson.getResponse()


class TweetListView(APIView):
    """
    get: Get all Tweet list
    """
    authentication_classes = (CustomJWTTokenAuthentication, )
    permission_classes = (permissions.AllowAny, )
    renderer_classes = (JSONRenderer, )

    def __init__(self):
        self.makejson = MakeJSON()

    def get(self, request):
        """
        sdfsdf
        """
        tweets = Tweet.objects.order_by("-id").all()

        data = TweetSerializer(tweets, many=True).data
        self.makejson.addResult(tweets=data)
        return self.makejson.getResponse()

