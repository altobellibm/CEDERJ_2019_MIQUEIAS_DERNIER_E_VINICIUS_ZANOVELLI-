from scraping import engine as microframework


class Pharmaceutical(microframework.Bot):
    @microframework.trigger('water_soludibility')
    def water_solubility(self, api):
        # logic based on DrugBank website (Aug 20, 2019)

        input_var = 'Solubility'
        condition = 'Approved'
        base_url = 'https://www.drugbank.ca'
        output = {}

        page = api.get(base_url)
        form = page.find_all('form', {'class': 'home-search-form'})
        search_url = base_url + form[0]['action']
        search_param = form[0].find_all('input')

        params = dict()
        for par in search_param:
            if par.has_attr('name') and par.has_attr('type'):
                value = ''
                if par.has_attr('value'):
                    if par['type'] == 'radio' or par['type'] == 'checkbox':
                        if par.has_attr('checked'):
                            value = par['value']
                    else:
                        value = par['value']
                params[par['name']] = value
        # print(params)  # manual dev debug

        payload = [('query', input_var), ('utf8', '✓'), ('searcher', 'drugs')]
        page = api.post(search_url, payload)
        api.log('Page reached: %s' % page.title.text)

        articles = page.find_all('div', {'class': 'search-result'})
        for a in articles:

            groups = a.find('div', {'class', 'hit-groups'})

            med = a.find('h2').find('a')
            name = med.text
            url = base_url + med['href']
            data = []

            if (len(groups.find_all('div')) != 1) or (groups.find('div').text.lower() != condition.lower()):
                api.log('-> Ignoring %s (doesn\'t match conditions)' % name)

            else:

                article = api.get(url)
                table = article.find('table', {'id': 'drug-moldb-properties'})

                check = getattr(table, "find_all", None)
                if callable(check):
                    for row in table.find_all('tr'):
                        cols = row.find_all('td')
                        cols = [val.text.strip() for val in cols]
                        data.append([val for val in cols if val])

                api.debug('Response sample: %s' % str(data)[:30])

                for record in data:
                    if len(record) > 0:
                        if input_var.lower() in record[0].lower():

                            output.update({
                                name: {
                                    'water_solubility': record[1],
                                    'url': url,
                                    'source': record[2],
                                }
                            })

                            api.log('-> %s: %s (source: %s)' % (name, record[1], record[2]))

        api.save_json(output)




scrap = Pharmaceutical(dict(
    charset='utf-8',
    parser='html5lib',  # html5lib | lxml | html.parser
    filesystem=dict(
        input='./input/',
        output='./output/',
        logs='./logs/',
        drivers=dict(
            geckodriver='../../vendor/geckodriver/0.24.0/',             # Firefox 65+
            chromedriver='../../vendor/chromedriver/76.0.3809.68/',     # Chrome 76
            # chromedriver='../../vendor/chromedriver/77.0.3865.10/',   # Chrome 77
            # safaridriver='',  # no support for Safari at this time
            # msdriver='',      # no support for Edge at this time
        ),
    ),
    verbose=True,
    debug=False,
))


if __name__ == "__main__":
    scrap.water_solubility()

