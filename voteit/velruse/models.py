from betahaus.pyracont.factories import createContent
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from voteit.core.models.auth import AuthPlugin
from voteit.core.models.interfaces import IUser

from voteit.velruse.exceptions import UserNotFoundError


class BaseOAuth2Plugin(AuthPlugin):
    name = ''

    def appstruct(self, auth_info):
        result = dict(
            oauth_token = auth_info['credentials']['oauthAccessToken'],
            oauth_userid = auth_info['profile']['accounts'][0]['userid'],
        )
        try:
            result['email'] = auth_info['profile']['verifiedEmail']
        except KeyError:
            pass
        return result
  
    def login(self, appstruct):
        user = self.context.users.get_auth_domain_user(self.name, 'oauth_userid', appstruct['oauth_userid'])
        if user:
            headers = remember(self.request, user.userid)
            url = appstruct.get('came_from', None)
            if url is None:
                url = self.request.resource_url(self.context)
            raise HTTPFound(location = url,
                             headers = headers)
        raise UserNotFoundError()
 
    def register(self, appstruct):
        name = appstruct.pop('userid')
        obj = createContent('User', creators=[name], **appstruct)
        self.context.users[name] = obj
        self.set_auth_domain(obj, self.name)
        return obj

    def set_auth_domain(self, user, domain, **kw):
        assert domain == self.name
        assert IUser.providedBy(user)
        auth_info = get_auth_info(self.request)
        reg_data = self.appstruct(auth_info)
        kw['oauth_userid'] = reg_data['oauth_userid']
        user.auth_domains[self.name] = kw


def get_auth_info(request):
    token = request.params['token']
    storage = request.registry.velruse_store
    return storage.retrieve(token)
