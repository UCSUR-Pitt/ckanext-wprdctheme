from setuptools import setup, find_packages

version = '0.2'

setup(
    name='ckanext-wprdc',
    version=version,
    description="The custom template for the WPRDC CKAN instance.",
    long_description='',
    classifiers=[],
    keywords='',
    author='Koury Lape',
    author_email='kll64@pitt.edu',
    url='',
    license='MIT',
    packages=find_packages(),
    namespace_packages=['ckanext', 'ckanext.wprdc'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points="""
        [ckan.plugins]
            wprdc=ckanext.wprdc.plugin:WPRDCPlugin
        [paste.paster_command]
            initdb=ckanext.wprdc.commands:InitDB
    """,
)