
from django.core.cache import cache
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CachedJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user_id = validated_token[api_settings.USER_ID_CLAIM]
        cache_key = f"jwt_user:{user_id}"

        user = cache.get(cache_key)

        if user is None:
            try:
                user = self.user_model.objects.get(
                    **{api_settings.USER_ID_FIELD: user_id}
                )
            except self.user_model.DoesNotExist:
                raise AuthenticationFailed("User not found")

            if not user.is_active:
                raise AuthenticationFailed("User is inactive")

            cache.set(cache_key, user, timeout=60)

        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        return user
