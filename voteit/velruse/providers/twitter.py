from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from velruse import login_url

from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.models import BaseOAuth2Plugin


class TwitterAuth(BaseOAuth2Plugin):
    name = 'twitter'
    title = _(u"Twitter")

    def render_login_info(self):
        return _login_btn(self.context, self.request)

    render_register_info = render_login_info

    def modify_register_schema(self, schema):
        """ There's no image plugin for twitter yet, so we're just overriding the subclassed function.
        """
        pass


def _login_btn(context, request):
    response = {'login_url': login_url(request, 'twitter')}
    return render("templates/twitter.pt", response, request = request)


@view_action('connect_forms', 'twitter', title = _(u"Twitter"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        return _login_btn(contex, request)


def includeme(config):
    config.registry.registerAdapter(TwitterAuth, name = TwitterAuth.name)
    config.scan(__name__)
