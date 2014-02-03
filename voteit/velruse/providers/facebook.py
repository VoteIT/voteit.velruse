from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from velruse import login_url
from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.models import BaseOAuth2Plugin


class FacebookAuth(BaseOAuth2Plugin):
    name = 'facebook'
    title = _(u"Facebook")

    def render_login_info(self):
        return _login_btn(self.context, self.request)

    render_register_info = render_login_info


@view_action('connect_forms', 'facebook', title = _(u"Facebook"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        return _login_btn(context, request)

def _login_btn(context, request):
    response = {'login_url': login_url(request, 'facebook')}
    return render("templates/facebook.pt", response, request = request)
    


def includeme(config):
    config.registry.registerAdapter(FacebookAuth, name = FacebookAuth.name)
    config.include('voteit.velruse.image_plugins.facebook') #As default?
    config.scan(__name__)
