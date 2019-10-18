def api_headless_browser(api):
    url = 'https://www.google.com/chrome/'
    headless_chrome = api.headless_browser('Chrome')
    headless_chrome.get(url)
    page_title = headless_chrome.title
    headless_chrome.quit()
    api.log('GET %s' % url)
    api.log('Page title is: %s' % page_title)
