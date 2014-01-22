from zope.interface import implementer
from voteit.core.models.auth import AuthPlugin


class VelruseAuthPlugin(AuthPlugin):
    name = 'velruse'



#@implementer(IAuthInfoExtractor)
#class AuthInfoExtractor(object):
#    
#    def __call__(self, auth_info):
#        raise NotImplementedError()


# class OAuth2Extractor(AuthInfoExtractor):
#     
#     def __call__(self, auth_info):
#         result = dict(
#             oauth_token = result['credentials']['oauthAccessToken'],
#             oauth_userid = result['profile']['accounts'][0]['userid'],
#         )
#         if 'verifiedEmail' in auth_info['profile']:
#             result['email'] = auth_info['profile']['verifiedEmail']
#         return result


def get_auth_info(request):
    token = request.params['token']
    storage = request.registry.velruse_store
    return storage.retrieve(token)