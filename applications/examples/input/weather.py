def weather(api):
    # logic based on Clima Tempo website (Aug 20, 2019)

    url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/313/niteroi-rj'
    page = api.get(url)

    temp_min = page.find('span', {'class': 'min-temp'}).text.split('\\')[0]
    temp_max = page.find('span', {'class': 'max-temp'}).text.split('\\')[0]
    temp = 'from %s to %s' % (temp_min, temp_max)

    api.log('-> According to Clima Tempo, weather temperature nearby UFF right now is %s Celsius degrees' % temp)

    api.save_json(dict(
        min_temp=temp_max,
        max_temp=temp_max
    ))
