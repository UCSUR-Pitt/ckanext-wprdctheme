import logging
import pylons.config as config
import ckan.plugins as p
import ckan.lib.helpers as h
from ckan.common import request
from datetime import date

log = logging.getLogger('ckanext.wprdc')

class WPRDCPlugin(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')

    def check_user_terms(self):
        if 'wprdc_user_terms' in request.cookies:
            return True
        else:
            controller = 'ckanext.wprdc.controller:WPRDCController'
            h.redirect_to(controller=controller, action='view_terms', came_from=request.url)

    def get_current_year(self):
        return date.today().year

    def get_wordpress_url(self):
        url = config.get('ckan.wordpress_url', 'http://www.wprdc.org')
        return url

    def get_helpers(self):
        return {
            'wprdc_user_terms': self.check_user_terms,
            'wprdc_get_year': self.get_current_year,
            'wprdc_wordpress_url': self.get_wordpress_url
        }

    def before_map(self, map):
        controller = 'ckanext.wprdc.controller:WPRDCController'
        map.redirect('/', '/dataset')
        map.connect(
            'terms', '/terms-of-use', controller=controller, action='view_terms', conditions=dict(method=['GET'])
        )
        map.connect(
            'terms', '/terms-of-use', controller=controller, action='submit_terms', conditions=dict(method=['POST'])
        )
        return map


