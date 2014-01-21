from pyramid.i18n import TranslationStringFactory

PROJECTNAME = 'voteit.velruse'
VoteITVelruseTSF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.scan(PROJECTNAME)
    #config.add_translation_dirs('%s:locale/' % PROJECTNAME)
#    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
#    config.add_static_view('voteit_velruse_static', '%s:static' % PROJECTNAME, cache_max_age = cache_ttl_seconds)
