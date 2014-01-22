import colander
import deform
from betahaus.viewcomponent import view_action
from betahaus.pyracont.factories import createContent
from pyramid.renderers import render
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from velruse import login_url
from voteit.core.models.auth import AuthPlugin
from voteit.core.models.interfaces import IUser

from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.exceptions import UserNotFoundError
from voteit.velruse.models import get_auth_info


class OpenID(AuthPlugin):
    name = 'openid'

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
        raise Exception()
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
        raise Exception()
        name = appstruct.pop('userid')
        obj = createContent('User', creators=[name], **appstruct)
        self.context.users[name] = obj
        self.set_auth_domain(obj, self.name)

    def set_auth_domain(self, user, domain, **kw):
        raise Exception()
        assert domain == self.name
        assert IUser.providedBy(user)
        auth_info = get_auth_info(self.request)
        reg_data = self.appstruct(auth_info)
        kw['oauth_userid'] = reg_data['oauth_userid']
        user.auth_domains[self.name] = kw

def add_openid_from_settings(config, prefix='velruse.openid.'):
    from velruse.settings import ProviderSettings
    settings = config.registry.settings
    p = ProviderSettings(settings, prefix)
    p.update('realm')
    p.update('storage')
    p.update('login_path')
    p.update('callback_path')
    config.add_openid_login(**p.kwargs)

@view_action('login_forms', 'openid', title = _(u"OpenID"))
def login_va(context, request, va, **kw):
    api = kw['api']
    if not api.userid:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'openid')}
        return render("templates/openid.pt", response, request = request)

@view_action('connect_forms', 'openid', title = _(u"OpenID"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'openid')}
        return render("templates/openid.pt", response, request = request)

def includeme(config):
    config.registry.registerAdapter(OpenID, name = OpenID.name)
    config.scan()