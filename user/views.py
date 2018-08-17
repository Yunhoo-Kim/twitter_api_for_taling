from rest_framework.views import APIView
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import UserSerializer, User
from tweet.serializers import UserPageSerializer

from helper.authentications import CustomJWTTokenAuthentication
from helper.makejson import MakeJSON
from helper.utils import jwt_response_payload_handler

import json


class SignupView(JSONWebTokenAPIView):
    """
    post: Signup
    """
    authentication_classes = (CustomJWTTokenAuthentication, )
    permission_classes = (permissions.AllowAny, )
    renderer_classes = (JSONRenderer, )
    serializer_class = UserSerializer

    def __init__(self):
        self.makejson = MakeJSON()

    def post(self, request):
        query = json.loads(request.body.decode("utf-8"))

        ser = UserSerializer(data=query)

        if not ser.is_valid():
            return self.makejson.get400ResponseWithResponse()

        ser.save()

        return self.makejson.getResponse()


class LoginView(JSONWebTokenAPIView):
    """
    post: login
    """
    authentication_classes = (CustomJWTTokenAuthentication, )
    permission_classes = (permissions.AllowAny, )
    renderer_classes = (JSONRenderer, )
    serializer_class = JSONWebTokenSerializer

    def __init__(self):
        self.makejson = MakeJSON()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            return Response(response_data)

        return self.makejson.get400ResponseWithResponse()


class UserPageView(APIView):
    """
    get : get User Page
    """
    authentication_classes = (CustomJWTTokenAuthentication, )
    permission_classes = (permissions.AllowAny, )
    renderer_classes = (JSONRenderer, )

    def __init__(self):
        self.makejson = MakeJSON()

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return self.makejson.get400ResponseWithResponse()

        self.makejson.addResult(data=UserPageSerializer(user).data)

        return self.makejson.getResponse()


class UserView(APIView):
    """
    get : get User Detail
    """
    authentication_classes = (CustomJWTTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    renderer_classes = (JSONRenderer, )

    def __init__(self):
        self.makejson = MakeJSON()

    def get(self, request):
        user = request.user
        self.makejson.addResult(data=UserPageSerializer(user).data)
        return self.makejson.getResponse()
