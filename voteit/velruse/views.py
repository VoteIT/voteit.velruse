from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.security import NO_PERMISSION_REQUIRED
from voteit.core.models.interfaces import IAuthPlugin
from voteit.core.models.interfaces import IFlashMessages

from .models import get_auth_info
from .exceptions import UserNotFoundError
from voteit.velruse import VoteITVelruseTSF as _


def includeme(config):
    config.add_view(logged_in,
                    route_name='logged_in')
    config.add_route('logged_in', '/logged_in')
    #FIXME: Add any other  generic badness...
    config.add_view(exception_view, context = 'openid.yadis.discover.DiscoveryFailure', permission = NO_PERMISSION_REQUIRED)
    config.add_view(exception_view, context = 'velruse.exceptions.VelruseException', permission = NO_PERMISSION_REQUIRED)

def _try_to_add_error(request, msg):
    fm = request.registry.queryAdapter(request, IFlashMessages)
    if fm:
        msg = _(u"third_party_login_error",
                 default="A third party request caused an error: '${msg}'",
                 mapping={'msg': msg})
        fm.add(msg, type = 'error')

def exception_view(context, request):
    _try_to_add_error(request, context.message)
    return HTTPFound(location = "/")

def logged_in(context, request):
    """ Handle login through another service. Note that this is not the same as a local login.
        A cookie still needs to be set. Also, it's possible to run this method for a user that's
        already logged in locally, ie wanting to connect to a another service to use it as auth.
    """
    userid = authenticated_userid(request)
    auth_info = get_auth_info(request)
    if 'error' in auth_info:
        _try_to_add_error(request, auth_info['error'])
        return HTTPFound(location = "/")
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
