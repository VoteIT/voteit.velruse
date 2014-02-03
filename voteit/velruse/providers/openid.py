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


class OpenIDAuth(AuthPlugin):
    name = 'openid'
    title = _(u"OpenID")

    def render_login_info(self):
        return _login_form(self.context, self.request)

    render_register_info = render_login_info

    def appstruct(self, auth_info):
        result = dict(
            openid_username = auth_info['profile']['accounts'][0]['username'],
        )
        #FIXME: Make this configurable through attribute exchange...
        try:
            result['email'] = auth_info['profile']['verifiedEmail']
        except KeyError:
            pass
        return result
  
    def login(self, appstruct):
        user = self.context.users.get_auth_domain_user(self.name, 'openid_username', appstruct['openid_username'])
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
        kw['openid_username'] = reg_data['openid_username']
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

def _login_form(context, request):
    response = {'login_url': login_url(request, 'openid')}
    return render("templates/openid.pt", response, request = request)

@view_action('connect_forms', 'openid', title = _(u"OpenID"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        return _login_form(context, request)

def includeme(config):
    config.registry.registerAdapter(OpenIDAuth, name = OpenIDAuth.name)
    config.scan(__name__)
