def api_start_browser(api):
    url = 'https://www.mozilla.org'
    ff = api.start_browser('Firefox')
    ff.get(url)
    page_title = ff.title
    ff.quit()
    api.log('GET %s' % url)
    api.log('Page title is: %s' % page_title)
