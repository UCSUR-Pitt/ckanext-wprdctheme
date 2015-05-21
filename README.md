# WPRDC CKAN Theme

This is an extension to CKAN that provides a custom theme for the Western Pennsylvania Regional Data Center. 


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
ckan.wordpress_url = http://<wordpress_url>
ckan.plugins = ... wprdc
```



