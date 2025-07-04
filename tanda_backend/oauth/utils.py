import time

from django.contrib.auth import get_user_model

UserModel = get_user_model()


def get_user_id_from_payload(payload):
    return payload.get("user_id")


def get_user_by_sso_id(sso_id):
    try:
        return UserModel.objects.get(sso_id=sso_id)
    except UserModel.DoesNotExist:
        return None


def refresh_has_expired(exp: int, context=None) -> bool:
    return time.time() > exp


def create_user_from_payload(payload):
    return UserModel.objects.create_user(
        sso_id=payload.get("public_id"),
        username=payload.get("username"),
        email=payload.get("email"),
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
    )


def set_user_sso_id(username, sso_id):
    if not username or not sso_id:
        return None
    try:
        user = UserModel.objects.get(username=username)
        user.sso_id = sso_id
        user.save()
    except UserModel.DoesNotExist:
        return None
    return user
