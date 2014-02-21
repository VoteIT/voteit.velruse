import colander
import deform
from betahaus.pyracont.factories import createContent
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from voteit.core.models.auth import AuthPlugin
from voteit.core.models.interfaces import IUser

from voteit.velruse.exceptions import UserNotFoundError
from voteit.velruse import VoteITVelruseTSF as _


@colander.deferred
def deferred_token_default(node, kw):
    request = kw['request']
    return request.params['token']


class BaseOAuth2Plugin(AuthPlugin):

    def appstruct(self, auth_info):
        result = dict(
            oauth_token = auth_info['credentials']['oauthAccessToken'],
            oauth_userid = auth_info['profile']['accounts'][0]['userid'],
        )
        try:
            result['email'] = auth_info['profile']['verifiedEmail']
        except KeyError:
            pass
        return result
  
    def login(self, appstruct):
        user = self.context.users.get_auth_domain_user(self.name, 'oauth_userid', appstruct['oauth_userid'])
        if user:
            headers = remember(self.request, user.userid)
            url = appstruct.get('came_from', None)
            if url is None:
                url = self.request.resource_url(self.context)
            raise HTTPFound(location = url,
                             headers = headers)
        raise UserNotFoundError()

    def modify_register_schema(self, schema):
        schema.add(colander.SchemaNode(colander.Bool(),
                                       name = 'use_profile_image',
                                       title = _(u"Use profile image"),
                                       description = _(u"use_profile_image_federated_description",
                                                       default = u"Your profile image will be set from this service. "
                                                           u"You can change this later of course."),
                                       default = True))
        schema.add(colander.SchemaNode(colander.String(),
                                       name = 'token',
                                       widget = deform.widget.HiddenWidget(),
                                       default = deferred_token_default))

    def register(self, appstruct):
        appstruct.pop('token', None) #Remove if it exists
        name = appstruct.pop('userid')
        use_profile_image = appstruct.pop('use_profile_image', True)
        if use_profile_image and 'profile_image_plugin' not in appstruct: #Ie allowed and not passed along
            appstruct['profile_image_plugin'] = self.name #Same as plugin name so far!
        obj = createContent('User', creators=[name], **appstruct)
        self.context.users[name] = obj
        self.set_auth_domain(obj, self.name)
        return obj

    def set_auth_domain(self, user, domain, **kw):
        assert domain == self.name
        assert IUser.providedBy(user)
        auth_info = get_auth_info(self.request)
        reg_data = self.appstruct(auth_info)
        kw['oauth_userid'] = reg_data['oauth_userid']
        user.auth_domains[self.name] = kw


def get_auth_info(request):
    token = request.params['token']
    storage = request.registry.velruse_store
    return storage.retrieve(token)
