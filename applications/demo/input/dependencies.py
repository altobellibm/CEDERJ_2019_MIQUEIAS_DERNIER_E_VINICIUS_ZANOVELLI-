import requests
import selenium
import bs4
import html5lib
import lxml


def dependencies(api):
    api.log('All the dependencies should be installed and available in the current environment')
    api.log('Requests: %s' % requests.__version__)
    api.log('Selenium: %s' % selenium.__version__)
    api.log('Beautiful Soup: %s' % bs4.__version__)
    api.log('html5lib: %s' % html5lib.__version__)
    api.log('lxml: %s' % '.'.join(str(v) for v in lxml.etree.LXML_VERSION))
