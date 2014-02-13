from voteit.core.models.profile_image import ProfileImagePlugin

from voteit.velruse import VoteITVelruseTSF as _


class GoogleProfileImagePlugin(ProfileImagePlugin):
    name = u'google_oauth2'
    title = _('Google')
    description = _(u"Your google profile image.")

    def url(self, size, request):
        if not 'google_oauth2' in self.context.auth_domains:
            return None
        oauth_userid = self.context.auth_domains['google_oauth2'].get('oauth_userid')
        if oauth_userid:
            return u'https://plus.google.com/s2/photos/profile/%(oauth_userid)s?sz=%(size)s' % {'oauth_userid': oauth_userid, 'size': size}
    
    def is_valid_for_user(self):
        if 'google_oauth2' in self.context.auth_domains:
            oauth_userid = self.context.auth_domains['google_oauth2']['oauth_userid']
            if oauth_userid:
                return True


def includeme(config):
    config.registry.registerAdapter(GoogleProfileImagePlugin, name = GoogleProfileImagePlugin.name)
