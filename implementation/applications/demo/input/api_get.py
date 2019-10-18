def api_get(api):
    page = api.get('http://uff.br/')
    api.log('Page title is: %s' % page.title.text)
