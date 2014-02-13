from voteit.core.models.profile_image import ProfileImagePlugin

from voteit.velruse import VoteITVelruseTSF as _


class FacebookProfileImagePlugin(ProfileImagePlugin):
    name = u'facebook_profile_image'
    title = _('Facebook')
    description = _(u'facebook_profile_image_description',
                    default=u"Your profile image is the same as the one you use on Facebook.")

    def url(self, size, request):
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

def includeme(config):
    config.registry.registerAdapter(FacebookProfileImagePlugin, name = FacebookProfileImagePlugin.name)
