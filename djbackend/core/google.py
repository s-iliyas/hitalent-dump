import requests
from oauth2client import client
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


GOOGLE_AUTH_URL = "https://www.googleapis.com/oauth2/v4/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


class GoogleLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_data = request.data
        data = {
            "code": request_data["code"],
            "client_id": "google_client_id",
            "client_secret": "google_client_secret",
            "redirect_uri": "http://34.201.128.125",
            "grant_type": "authorization_code",
        }
        response = requests.post(GOOGLE_AUTH_URL, data=data)
        if not response.ok:
            return Response(
                {"message": "Failed to obtain access token from Google."},
                status=status.HTTP_200_OK,
            )
        accessToken = response.json()["accessToken"]
        payload = {"accessToken": accessToken}  # validate the token
        r = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo", params=payload
        )
        data = json.loads(r.text)
        if "error" in data:
            content = {
                "message": "wrong google token / this google token is already expired."
            }
            return Response(content)
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            user = User()
            user.username = data["email"]
            # provider random default password
            user.password = make_password(
                BaseUserManager().make_random_password())
            user.email = data["email"]
            user.save()
        token = RefreshToken.for_user(
            user
        )  # generate token without username & password
        response = {}
        response["username"] = user.username
        response["accessToken"] = str(token.accessToken)
        response["refresh_token"] = str(token)
        return Response(response)


def calender(token):
    credentials = client.AccessTokenCredentials(token, "USER_AGENT")
    service = build("calendar", "v3", credentials=credentials)
    google_calendar_events = (
        service.events()
        .list(calendarId="primary", singleEvents=True, orderBy="startTime")
        .execute()
    )
    google_calendar_events = google_calendar_events.get("items", [])
    print(google_calendar_events)
