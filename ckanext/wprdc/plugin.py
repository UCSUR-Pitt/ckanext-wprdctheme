import logging
import re
import urllib
import urllib2
import json
import datetime

import pylons.config as config
import ckan.lib.captcha as captcha
import ckan.plugins as p
import ckan.lib.helpers as h

from ckan.common import request
from dateutil import tz

log = logging.getLogger('ckanext.wprdc')

def check_if_google():
    regex = re.compile("bot|crawl|slurp|spider|python", re.IGNORECASE)
    r = regex.search(request.environ.get('HTTP_USER_AGENT', ''))
    if r:
        return True
    else:
        return False


class WPRDCPlugin(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IPackageController, inherit=True)

    # IConfigurer
    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_resource('fanstatic', 'wprdc_theme')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'wprdc_user_terms': self.check_user_terms,
            'wprdc_get_year': self.get_current_year,
            'wprdc_wordpress_url': self.get_wordpress_url,
            'wprdc_google_tracking': self.get_google_tracking,
            'render_datetime': self.convert_to_local,
        }

    def check_user_terms(self):
        if check_if_google():
            return True
        else:
            if 'wprdc_user_terms' in request.cookies:
                return True
            else:
                return False
                # request_uri = request.environ.get('REQUEST_URI', '')
                # controller = 'ckanext.wprdc.controller:WPRDCController'
                # #h.redirect_to(controller=controller, action='view_terms', came_from=request.url)
                # h.redirect_to(controller=controller, action='view_terms', came_from=request_uri)

    def get_current_year(self):
        return datetime.date.today().year

    def get_wordpress_url(self):
        url = config.get('ckan.wordpress_url', 'http://www.wprdc.org')
        return url

    def get_google_tracking(self):
        url = config.get('ckan.google_tracking', '')
        return url

    def convert_to_local(self, time, date_format=None, with_hours=False):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = h._datestamp_to_datetime(str(time))

        if not utc:
            return ''

        utc = utc.replace(tzinfo=from_zone)
        time = utc.astimezone(to_zone)

        # if date_format was supplied we use it
        if date_format:
            return time.strftime(date_format)

        # if with_hours was supplied show them
        if with_hours:
            return time.strftime('%B %-d, %Y, %-I:%M %p')
        else:
            return time.strftime('%B %-d, %Y')

    # IRoutes
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

    # IPackageController
    def after_create(self, context, pkg_dict):
        if 'group' in pkg_dict:
            if pkg_dict['group']:
                data = {
                    'id': pkg_dict['group'],
                    'object': pkg_dict['id'],
                    'object_type': 'package',
                    'capacity': 'public'
                }
                p.toolkit.get_action('member_create')(context, data)

    def after_update(self, context, pkg_dict):
        if 'group' in pkg_dict:
            if pkg_dict['group']:
                data = {
                    'id': pkg_dict['group'],
                    'object': pkg_dict['id'],
                    'object_type': 'package',
                    'capacity': 'public'
                }
                p.toolkit.get_action('member_create')(context, data)
            self.remove_from_other_groups(context, pkg_dict['id'])

    def remove_from_other_groups(self, context, package_id):
        package = p.toolkit.get_action('package_show')(context, {'id': package_id})
        for group in package['groups']:
            if group['name'] != package['group']:
                p.toolkit.get_action('member_delete')(context, {'id': group['id'], 'object': package['id'], 'object_type': 'package'})

# monkey patch till CKAN v2.5 stable release
def replace_check_recaptcha(request):
    recaptcha_private_key = config.get('ckan.recaptcha.privatekey', '')
    if not recaptcha_private_key:
        return
    client_ip_address = request.environ.get('REMOTE_ADDR', 'Unknown IP Address')
    recaptcha_response_field = request.params.get('g-recaptcha-response', '')
    recaptcha_server_name = 'https://www.google.com/recaptcha/api/siteverify'
    params = urllib.urlencode(dict(secret=recaptcha_private_key,
                                   remoteip=client_ip_address,
                                   response=recaptcha_response_field.encode('utf8')))
    f = urllib2.urlopen(recaptcha_server_name, params)
    data = json.load(f)
    f.close()
    try:
        if not data['success']:
            raise captcha.CaptchaError()
    except IndexError:
        raise captcha.CaptchaError()

captcha.check_recaptcha = replace_check_recaptcha
