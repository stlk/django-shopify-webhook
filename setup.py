from setuptools import setup, find_packages

version = __import__('shopify_webhook').__version__

setup(
    name = 'django-shopify-webhook',
    version = version,
    description = 'A package for the creation of Shopify Apps using the Embedded App SDK.',
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'Gavin Ballard',
    author_email = 'gavin@discolabs.com',
    url = 'https://github.com/stlk/django-shopify-webhook',
    license = 'None',

    packages = find_packages(),

    install_requires = [
        'django >=3.2',
        'setuptools >=5.7'
    ],

    zip_safe = True,
    classifiers = [],
)
