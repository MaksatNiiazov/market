import graphene

from .mixins import ObtainJSONWebTokenMixin
from .mixins import RefreshMixin


class ObtainJSONWebTokenMutation(ObtainJSONWebTokenMixin, graphene.Mutation):
    """Obtain JSON Web Token mutation"""

    @classmethod
    def Field(cls, *args, **kwargs):  # noqa: N802
        cls._meta.arguments.update(
            {
                "authorization_code": graphene.String(required=True),
                "redirect_uri": graphene.String(required=True),
            },
        )
        return super().Field(*args, **kwargs)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)


class Refresh(RefreshMixin, graphene.Mutation):
    class Arguments:
        """Refresh Arguments"""

        token = graphene.String()

    @classmethod
    def mutate(cls, *arg, **kwargs):
        return cls.refresh(*arg, **kwargs)
