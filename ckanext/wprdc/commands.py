import logging
import ckan.model as model
import ckan.plugins as p

log = logging.getLogger('ckanext.wprdc')

class InitDB(p.toolkit.CkanCommand):
    """Setup the database table for storing User Agreements

    Usage::
        paster dbinit
            Creates the necessary tables for storing when a user accepts the
            terms of use.

    The commands should be run from the ckanext-wprdc directory and expect
    a development.ini file to be present. Most of the time you will
    specify the config explicitly though::

    paster dbinit -c /etc/ckan/default/development.ini
    """

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 0
    min_args = 0

    def command(self):
        self._load_config()

        model.Session.remove()
        model.Session.configure(bind=model.meta.engine)

        import ckanext.wprdc.model as m
        m.init_tables()
        log.info("DB tables are setup")


