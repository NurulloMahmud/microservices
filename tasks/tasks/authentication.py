# tasks/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import exceptions
import requests
from django.conf import settings

class SimpleUser:
    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role
        self.is_authenticated = True  # Ensure compatibility with `IsAuthenticated` permission

class CustomUserJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get and validate the token from the request
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        print("raw token: ", raw_token)

        try:
            validated_token = self.get_validated_token(raw_token)
            print("validated token: ", validated_token)
        except exceptions.AuthenticationFailed:
            print("Authentication failed")
            raise AuthenticationFailed("Invalid token")

        # Extract user_id and role from the token payload
        user_id = validated_token.get("user_id")
        role = validated_token.get("role")
        print("user_id: ", user_id)
        print("role: ", role)

        # Verify user information with `users` service
        user_info = self._fetch_user_info(user_id, raw_token.decode('utf-8'))

        # Create a custom user object with the user_id and role
        return (SimpleUser(user_id=user_id, role=role), validated_token)

    def _fetch_user_info(self, user_id, token):
        """
        Fetches additional user details from `users` service.
        """
        url = f"{settings.USERS_SERVICE_URL}/users/user/{user_id}/"  # Ensure correct URL
        headers = {'Authorization': f'Bearer {token}'}

        print("Fetching user info from users service...")
        print("URL: ", url)
        print("Headers: ", headers)

        try:
            response = requests.get(url, headers=headers)
            print("Response status code:", response.status_code)
            print("Response content:", response.content)

            response.raise_for_status()  # Raises an error for non-2xx responses
            return response.json()
        except requests.RequestException as e:
            print("Error fetching user info:", e)
            raise AuthenticationFailed("Failed to fetch user info from users service")
