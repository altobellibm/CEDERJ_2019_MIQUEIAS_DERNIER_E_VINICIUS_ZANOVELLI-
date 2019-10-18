def science(api):
    # logic based on Nasa website (Aug 20, 2019)

    base_url = 'https://science.nasa.gov'
    target_url = base_url + '/science-news'

    page = api.get(target_url)
    div = page.find('div', {'class': 'views-field-title'})
    span = div.find('span', {'class': 'field-content'})
    a = span.find('a')

    api.log('-> News from Nasa: %s' % a.text)
    api.log('-> Read more at: %s' % base_url + a['href'])

    api.save_json(dict(
        article=a.text,
        url=base_url + a['href'],
    ))
