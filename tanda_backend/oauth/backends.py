from django.contrib.auth import get_user_model

from .utils import get_user_by_sso_id

UserModel = get_user_model()


class SSOBackend:
    def authenticate(self, request=None, **kwargs):
        if request is None or not getattr(request, "_jwt_token_auth", False):
            return None

        sso_id = kwargs.get("sso_id")
        if sso_id is not None:
            return get_user_by_sso_id(sso_id)

        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
