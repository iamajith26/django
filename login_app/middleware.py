from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth.middleware import get_user

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authenticator = JWTAuthentication()

    def __call__(self, request):
        # Attach user to request based on JWT
        request.user = SimpleLazyObject(lambda: self.get_jwt_user(request))
        return self.get_response(request)

    def get_jwt_user(self, request):
        # If user is already authenticated (e.g., via session), return it
        user = get_user(request)
        if user.is_authenticated:
            return user

        # Check for JWT in Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return user  # Return anonymous user if no valid header

        try:
            # Extract token and authenticate using SimpleJWT's JWTAuthentication
            token = auth_header.split('Bearer ')[1]
            validated_token = self.jwt_authenticator.get_validated_token(token)
            user = self.jwt_authenticator.get_user(validated_token)
            if not user.is_active:
                return user  # Return anonymous user if inactive
            return user
        except (IndexError, InvalidToken, AuthenticationFailed):
            return user  # Return anonymous user on invalid token