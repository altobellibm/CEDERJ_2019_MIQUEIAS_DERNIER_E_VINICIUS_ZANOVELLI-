def api_post(api):
    url = 'https://www.w3schools.com/action_page.php'
    params = {
        'first_name': 'John',
        'last_name': 'Doe',
    }
    page = api.post(url, params)
    result = page.find('div').text
    api.log('Response: %s' % result)
