import sys

from ast import literal_eval
from setuptools import setup

VERSION = '0.1.0'

PACKAGES = [
    'scraping',
    'scraping.test'
]

SCRIPTS = []

REQUIREMENTS = 'requirements.json'

DEPENDENCIES = literal_eval(open(REQUIREMENTS, 'r', encoding='utf-8').read())

if sys.version_info < tuple(map(int, DEPENDENCIES['python'].split('.'))):
    sys.exit('Python %s+ is required (version %s found)\n'
             'Please update Python and try again' %
             (DEPENDENCIES['python'], '.'.join(map(str, sys.version_info[:3]))))

setup(
    name='Scraping',
    version=VERSION,
    author='',
    author_email='',
    packages=PACKAGES,
    scripts=SCRIPTS,
    description='A Microframework for Web Scraping',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    install_requires=[' >= '.join([kv, DEPENDENCIES['packages'][kv]])
                      for kv in DEPENDENCIES['packages']],
)
