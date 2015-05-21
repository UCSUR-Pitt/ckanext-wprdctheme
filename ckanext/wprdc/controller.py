import logging
import ckan.lib.base as base
import ckan.lib.helpers as h
from ckanext.wprdc.model import UserAgreement
from ckan.common import _, request, response

log = logging.getLogger('ckanext.wprdc')

class WPRDCController(base.BaseController):

    def view_terms(self):
        return base.render('terms/index.html')

    def submit_terms(self):
        ua = UserAgreement()
        came_from = request.params.get('came_from', h.url('/'))
        if not came_from:
            base.abort(400, _('Missing Value') + ': url')
        if h.url_is_local(came_from):
            ua.insert_new_agreement()
            response.set_cookie('wprdc_user_terms', 'true')
            return base.redirect(came_from)
        else:
            base.abort(403, _('Redirecting to external site is not allowed.'))