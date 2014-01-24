from betahaus.viewcomponent import view_action
from pyramid.renderers import render
from velruse import login_url
from zope.interface import implementer
from zope.component import adapter

from voteit.core.models.interfaces import IProfileImage
from voteit.core.models.interfaces import IUser

from voteit.velruse import VoteITVelruseTSF as _
from voteit.velruse.models import BaseOAuth2Plugin


class FacebookAuth(BaseOAuth2Plugin):
    name = 'facebook'


@implementer(IProfileImage)
@adapter(IUser)
class FacebookProfileImagePlugin(object):
    name = u'facebook_profile_image'
    title = _('Facebook')
    description = _(u'facebook_profile_image_description',
                    default=u"Your profile image is the same as the one you use on Facebook.")
    
    def __init__(self, context):
        self.context = context
    
    def url(self, size):
        if not 'facebook' in self.context.auth_domains:
            return None
        oauth_userid = self.context.auth_domains['facebook'].get('oauth_userid')
        if oauth_userid:
            return u'http://graph.facebook.com/%(UID)s/picture' % {'UID': oauth_userid}
    
    def is_valid_for_user(self):
        if 'facebook' in self.context.auth_domains:
            oauth_userid = self.context.auth_domains['facebook']['oauth_userid']
            if oauth_userid:
                return True
        return False


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
    config.registry.registerAdapter(FacebookProfileImagePlugin, name = FacebookProfileImagePlugin.name)
    config.scan()
