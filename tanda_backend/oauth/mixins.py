import graphene
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from graphene.types.generic import GenericScalar
from graphene.utils.thenables import maybe_thenable
from graphql.type.definition import GraphQLResolveInfo
from graphql_jwt import exceptions
from graphql_jwt import signals
from graphql_jwt.decorators import csrf_rotation
from graphql_jwt.decorators import ensure_token
from graphql_jwt.decorators import setup_jwt_cookie
from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import get_payload
from graphql_jwt.utils import get_user_by_payload

from .jwt import get_jwt
from .jwt import get_jwt_by_refresh
from .utils import create_user_from_payload
from .utils import set_user_sso_id


class JSONWebTokenMixin:
    """Mixin for JSON Web Token mutations."""

    payload = GenericScalar(required=True)

    @classmethod
    def Field(cls, *args, **kwargs):  # noqa: N802
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields["access_token"] = graphene.Field(
                graphene.String,
                required=True,
            )
            cls._meta.fields["refresh_token"] = graphene.Field(
                graphene.String,
                required=True,
            )
        return super().Field(*args, **kwargs)


class ObtainJSONWebTokenMixin(JSONWebTokenMixin):
    """Mixin for obtaining JSON Web Token mutations."""

    @classmethod
    def __init_subclass_with_meta__(cls, name=None, **options):
        assert getattr(cls, "resolve", None), (
            f"{name or cls.__name__}.resolve method is required in a JSONWebTokenMutation."
        )

        super().__init_subclass_with_meta__(name=name, **options)

    @classmethod
    @setup_jwt_cookie
    @csrf_rotation
    def resolve(cls, root, info: GraphQLResolveInfo, authorization_code: str, redirect_uri: str, **kwargs):
        """Resolve the JSON Web Token mutation.

        Args:
            root (_type_): root value supplied to the executor for the query.
            info (GraphQLResolveInfo): Information about the execution state of the query.
            authorization_code (str): authorization code from SSO service
            redirect_uri (str): redirect uri after authorization
            **kwargs: Arbitrary keyword arguments.
        """

        def on_token_auth_resolve(values):
            tokens, payload = values
            payload.access_token = tokens.pop("access_token")
            payload.refresh_token = tokens.pop("refresh_token")
            payload.payload = tokens
            return payload

        context = info.context
        context._jwt_token_auth = True
        tokens = get_jwt(authorization_code, redirect_uri)
        sso_id = tokens.get("user", {}).get("public_id")
        if not tokens or not sso_id:
            raise exceptions.JSONWebTokenError(
                _("SSO service is not available"),
            )

        user = authenticate(
            request=context,
            sso_id=sso_id,
        )
        if user is None:
            user = set_user_sso_id(tokens["user"].get("username"), sso_id)
            if not user:
                user = create_user_from_payload(tokens["user"])
            context.user = user

        if hasattr(context, "user"):
            context.user = user

        result = cls(payload=tokens["user"])
        signals.token_issued.send(sender=cls, request=context, user=user)
        return maybe_thenable((tokens, result), on_token_auth_resolve)


class KeepAliveRefreshMixin:
    """Mixin for refreshing JSON Web Token mutations."""

    class Fields:
        access_token = graphene.String()
        refresh_token = graphene.String()

    @classmethod
    @setup_jwt_cookie
    @csrf_rotation
    @ensure_token
    def refresh(cls, root, info: GraphQLResolveInfo, token: str, **kwargs):
        """Refresh the JSON Web Token mutation

        Args:
            root (_type_): root value supplied to the executor for the query.
            info (GraphQLResolveInfo): Information about the execution state of the query.
            token (str): refresh token
            **kwargs: Arbitrary keyword arguments.
        """

        def on_resolve(values):
            payload, access_token, refresh_token = values
            payload.access_token = access_token
            payload.refresh_token = refresh_token
            return payload

        context = info.context
        payload = get_payload(token, context)
        user = get_user_by_payload(payload)
        exp = payload.get("exp")

        if not exp:
            raise exceptions.JSONWebTokenError(_("exp field is required"))

        if jwt_settings.JWT_REFRESH_EXPIRED_HANDLER(exp, context):
            raise exceptions.JSONWebTokenError(_("Refresh has expired"))

        tokens = get_jwt_by_refresh(token)
        if tokens is None or not tokens.get("access_token") or not tokens.get("refresh_token"):
            raise exceptions.JSONWebTokenError(_("Error with sso servise"))
        signals.token_refreshed.send(sender=cls, request=context, user=user)

        result = cls(payload=payload)
        return maybe_thenable(
            (result, tokens["access_token"], tokens["refresh_token"]),
            on_resolve,
        )


class RefreshMixin(
    KeepAliveRefreshMixin,
    JSONWebTokenMixin,
):
    """RefreshMixin"""
