from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from velruse import login_url
from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.models import BaseOAuth2Plugin


class FacebookAuth(BaseOAuth2Plugin):
    name = 'facebook'


@view_action('login_forms', 'facebook', title = _(u"Facebook"))
def login_va(context, request, va, **kw):
    api = kw['api']
    if not api.userid:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'facebook')}
        return render("templates/generic.pt", response, request = request)

@view_action('connect_forms', 'facebook', title = _(u"Facebook"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'facebook')}
        return render("templates/generic.pt", response, request = request)

def includeme(config):
    config.registry.registerAdapter(FacebookAuth, name = FacebookAuth.name)
    config.include('voteit.velruse.image_plugins.facebook') #As default?
    config.scan()
