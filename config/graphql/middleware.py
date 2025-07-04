import logging


class GraphQLErrorMiddleware:
    def resolve(self, next, root, info, **args):
        try:
            return next(root, info, **args)
        except Exception as e:
            logging.error(f"GraphQL error: {str(e)}", exc_info=True)
            raise
