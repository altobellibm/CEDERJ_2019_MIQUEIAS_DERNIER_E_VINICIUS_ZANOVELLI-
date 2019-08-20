def api_render(api):
    page = api.render('https://google.com')
    api.log('Page title is: %s' % page.title.text)
