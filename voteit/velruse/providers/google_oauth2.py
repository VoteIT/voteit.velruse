from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from velruse import login_url

from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.models import BaseOAuth2Plugin


class GoogleOAuth2(BaseOAuth2Plugin):
    name = 'google_oauth2'


@view_action('login_forms', 'google_oauth2', title = _(u"Google"))
def login_va(context, request, va, **kw):
    api = kw['api']
    if not api.userid:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'google')}
        return render("templates/generic.pt", response, request = request)

@view_action('connect_forms', 'google_oauth2', title = _(u"Google"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'google')}
        return render("templates/generic.pt", response, request = request)

def includeme(config):
    config.registry.registerAdapter(GoogleOAuth2, name = GoogleOAuth2.name)
    config.include('voteit.velruse.image_plugins.google') #As default?
    config.scan()
