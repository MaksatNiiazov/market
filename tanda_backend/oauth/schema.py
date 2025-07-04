import graphene
import graphql_jwt

from .mutations import ObtainJSONWebTokenMutation
from .mutations import Refresh


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebTokenMutation.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = Refresh.Field()


schema = graphene.Schema(mutation=Mutation)
