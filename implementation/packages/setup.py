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

setup(
    name='Scraping',
    python_requires=DEPENDENCIES['python'],
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
