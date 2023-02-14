import json
import requests
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from ht_intern.models import InternLinkedInCred
from ht_hr.models import Intern, HrLinkedInCred
from ht_admin.models import Hr


class LinkedInCallback(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_data = request.data
        data = {
            "grant_type": "authorization_code",
            "code": request_data["code"],
            "redirect_uri": "http://localhost/auth/linkedin/callback",
            "client_id": "linkedin_client_id",
            "client_secret": "linkedin_client_secret",
        }
        res = requests.post(
            "http://www.linkedin.com/oauth/v2/accessToken",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=data,
        )
        token_obj = json.loads(res.text)
        if "id_token" in token_obj:
            decoded = jwt.decode(
                token_obj["id_token"], options={"verify_signature": False}
            )
            if "email" in decoded:
                cred_dict = {
                    "name": decoded["name"],
                    "email": decoded["email"],
                    "locale": decoded["locale"],
                    "accessToken": token_obj["accessToken"],
                    "expires_in": token_obj["expires_in"],
                    "token_type": token_obj["token_type"],
                    "id_token": token_obj["id_token"],
                }
                try:
                    hr = Hr.objects.get(email=decoded["email"])
                    try:
                        already_hr = HrLinkedInCred.objects.get(
                            email=decoded["email"])
                        already_hr.accessToken = token_obj["accessToken"]
                        already_hr.expires_in = token_obj["expires_in"]
                        already_hr.id_token = token_obj["id_token"]
                        already_hr.save(
                            update_fields=["accessToken",
                                           "id_token", "expires_in"]
                        )
                        userType = "hr"
                    except HrLinkedInCred.DoesNotExist:
                        HrLinkedInCred.objects.create(**cred_dict)
                        userType = "hr"
                except Hr.DoesNotExist:
                    try:
                        intern = Intern.objects.get(email=decoded["email"])
                        try:
                            already_intern = InternLinkedInCred.objects.get(
                                email=decoded["email"]
                            )
                            already_intern.accessToken = token_obj["accessToken"]
                            already_intern.expires_in = token_obj["expires_in"]
                            already_intern.id_token = token_obj["id_token"]
                            already_intern.save(
                                update_fields=["accessToken",
                                               "id_token", "expires_in"]
                            )
                            userType = "intern"
                        except InternLinkedInCred.DoesNotExist:
                            InternLinkedInCred.objects.create(**cred_dict)
                            userType = "intern"
                    except Intern.DoesNotExist:
                        return Response(
                            {
                                "message": "Please do contact with our HR (admin@hitalent.org)"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                try:
                    user = User.objects.get(email=decoded["email"])
                except User.DoesNotExist:
                    user = User()
                    user.username = decoded["email"]
                    user.email = decoded["email"]
                    user.password = make_password(
                        BaseUserManager().make_random_password()
                    )
                    user.save()
                token = RefreshToken.for_user(user)
                response = {}
                response["username"] = user.username
                response["accessToken"] = str(token.accessToken)
                response["refresh_token"] = str(token)
                response["userType"] = userType
                return Response({"tokens": response}, status=status.HTTP_200_OK)

            else:
                return Response(
                    {"message": "Please add email in your email account"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response({"message": token_obj}, status=status.HTTP_400_BAD_REQUEST)
