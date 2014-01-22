from pyramid.i18n import TranslationStringFactory
from velruse.app import find_providers

PROJECTNAME = 'voteit.velruse'
VoteITVelruseTSF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    from pyramid.security import NO_PERMISSION_REQUIRED
    from voteit.core.security import MANAGE_SERVER
    from velruse.app import auth_complete_view
    from velruse.app import auth_denied_view
    from velruse.app import auth_info_view
    config.include(configure_providers)
    config.include('velruse.app')
    config.commit() #To allow overrides of velruse
    #Override registrations with other permissions
    config.add_view(
        auth_complete_view,
        context = 'velruse.AuthenticationComplete',
        permission = NO_PERMISSION_REQUIRED)
    config.add_view(
        auth_denied_view,
        context = 'velruse.AuthenticationDenied',
        permission = NO_PERMISSION_REQUIRED)
    config.add_view(
        auth_info_view,
        name = 'auth_info',
        request_param  = 'format=json',
        renderer = 'json',
        permission = MANAGE_SERVER)
    config.include('%s.views' % PROJECTNAME)
    config.include(include_providers)
   #config.add_translation_dirs('%s:locale/' % PROJECTNAME)
 #   cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
#    config.add_static_view('voteit_velruse_static', '%s:static' % PROJECTNAME, cache_max_age = cache_ttl_seconds)

def configure_providers(config):
    import ConfigParser
    from paste.deploy.loadwsgi import NicerConfigParser
    from os.path import isfile
    settings = config.registry.settings
    file_name = settings.get('velruse_providers', 'etc/velruse_providers.ini')
    if not isfile(file_name):
        print u"voteit.velruse can't find any login providers file at: %s - won't add or configure any providers" % file_name
        return
    parser = ConfigParser.ConfigParser()
    parser.read(file_name)
    if 'velruse_providers' not in parser.sections():
        raise ValueError("Couldn't find any section with [velruse_providers] - see voteit.velruse documentation on configuration.")
    settings.update(parser.items('velruse_providers'))
    if 'session.secret' not in settings:
        from voteit.core import read_salt
        settings['session.secret'] =  read_salt(settings)
    if 'endpoint' not in settings:
        settings['endpoint'] = '/logged_in'
    from velruse.app import settings_adapter
    #THis is a hack and should perhaps be filed as a bug report to velruse
    if 'openid' not in settings_adapter:
        from .providers.openid import add_openid_from_settings
        settings_adapter['openid'] = 'add_openid_from_settings'
        config.add_directive('add_openid_from_settings',
                             add_openid_from_settings)

def include_providers(config):
    for provider in find_providers(config.registry.settings):
        #Check for import errors or do this another way?
        name = '%s.providers.%s' % (PROJECTNAME, provider)
        print "Including: %s" % name
        config.include(name)
