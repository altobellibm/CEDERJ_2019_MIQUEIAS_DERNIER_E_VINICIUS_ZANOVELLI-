def financial(api):
    # logic based on UOL website (Aug 20, 2019)

    url = 'https://economia.uol.com.br/cotacoes/cambio/'
    page = api.get(url)

    section = page.find('section', {'class': 'currency-converter'})
    span = section.find('div', {'class': 'currency-field2'})
    input_field = section.find('input', {'name': 'currency2'})
    brl = input_field['value']

    api.log('-> According to UOL, right now 1 USD = %s BRL' % brl)

    api.save_json(dict(
        usd=1,
        brl=brl
    ))
