from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from velruse import login_url

from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.models import BaseOAuth2Plugin


class GoogleOAuth2(BaseOAuth2Plugin):
    name = 'google_oauth2'
    title = _(u"Google")

    def render_login_info(self):
        return _login_btn(self.context, self.request)

    render_register_info = render_login_info


def _login_btn(context, request):
    response = {'login_url': login_url(request, 'google')}
    return render("templates/google.pt", response, request = request)


@view_action('connect_forms', 'google_oauth2', title = _(u"Google"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        return _login_btn(context, request)


def includeme(config):
    config.registry.registerAdapter(GoogleOAuth2, name = GoogleOAuth2.name)
    config.include('voteit.velruse.image_plugins.google') #As default?
    config.scan(__name__)
