from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from voteit.core.models.interfaces import IAuthPlugin

from .models import get_auth_info
from .exceptions import UserNotFoundError


def includeme(config):
    config.add_view(logged_in,
                    route_name='logged_in')
    config.add_route('logged_in', '/logged_in')


def logged_in(context, request):
    """ Handle login through another service. Note that this is not the same as a local login.
        A cookie still needs to be set. Also, it's possible to run this method for a user that's
        already logged in locally, ie wanting to connect to a another service to use it as auth.
    """
    #FIXME:
#     error_dict = {
#         'provider_type': context.provider_type,
#         'provider_name': context.provider_name,
#         'error': context.reason,
#     }
    userid = authenticated_userid(request)
    auth_info = get_auth_info(request)
    auth_method = request.registry.queryMultiAdapter((context, request), IAuthPlugin, name = auth_info['provider_type'])
    if not userid:
        appstruct = auth_method.appstruct(auth_info)
        try:
            return auth_method.login(appstruct)
        except UserNotFoundError:
            #May need to register?
            url = request.resource_url(context, 'register', auth_info['provider_type'], query = {'token': request.params['token']})
            return HTTPFound(location = url)
    else:
        user = context.users[userid]
        auth_method.set_auth_domain(user, auth_info['provider_type'])
        url = request.resource_url(user)
        return HTTPFound(location = url)
