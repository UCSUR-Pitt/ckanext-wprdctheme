# WPRDC CKAN Theme

This is an extension to CKAN that provides a custom theme for the Western Pennsylvania Regional Data Center. This extension makes use of the [ckanext-scheming](https://github.com/open-data/ckanext-scheming) extension. 


## Installation

To install ckanext-wprdctheme

```bash
source /usr/lib/ckan/default/bin/activate
pip install -e git+https://github.com/UCSUR-Pitt/ckanext-wprdctheme#egg=ckanext-wprdctheme
cd /usr/lib/ckan/default/src/ckanext-wprdctheme
paster initdb -c /etc/ckan/default/production.ini
```

Edit your CKAN Configuration .INI file

```bash
ckan.ckan.api_key = <admin_api_key>
ckan.wordpress_url = http://<wordpress_url>
ckan.google_tracking = UA-00000000-01
ckan.plugins = ... wprdc
scheming.dataset_schemas = ckanext.wprdc:dataset_schema.json
scheming.presets = ckanext.wprdc:dataset_presets.json
```


### CKAN Extensions

* [ckanext-scheming](https://github.com/open-data/ckanext-scheming)
* [ckanext-odata](https://github.com/jqnatividad/ckanext-odata)
* [ckanext-disqus](https://github.com/ckan/ckanext-disqus)
* [ckanext-datarequests](https://github.com/conwetlab/ckanext-datarequests)


