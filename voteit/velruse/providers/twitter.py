from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from velruse import login_url

from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.models import BaseOAuth2Plugin


class TwitterAuth(BaseOAuth2Plugin):
    name = 'twitter'

    def modify_register_schema(self, schema):
        """ There's no image plugin for twitter yet, so we're just overriding the subclassed function.
        """
        pass


@view_action('login_forms', 'twitter', title = _(u"Twitter"))
def login_va(context, request, va, **kw):
    api = kw['api']
    if not api.userid:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'twitter')}
        return render("templates/generic.pt", response, request = request)

@view_action('connect_forms', 'twitter', title = _(u"Twitter"))
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        response = {'provider': va.name,
                    'login_url': login_url(request, 'twitter')}
        return render("templates/generic.pt", response, request = request)

def includeme(config):
    config.registry.registerAdapter(TwitterAuth, name = TwitterAuth.name)
    config.scan(__name__)
