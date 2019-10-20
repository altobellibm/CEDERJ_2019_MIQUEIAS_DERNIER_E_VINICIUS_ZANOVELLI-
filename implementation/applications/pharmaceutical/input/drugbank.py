# This file is unfinished (work in progress)

# KNOWN-ISSUES:
# - Apparently not looping through all results or failing to check the "conditions"
# - Not handling pagination yet
# - Not filtering by time frame

# @trigger
def drugbank(api, settings):
    # drugbank, outubro de 2019
    farmacos = settings['fontes']['drugbank'].get('farmacos',[])
    propriedades = settings['fontes']['drugbank'].get('propriedades',[])
    base_url = 'https://www.drugbank.ca'
    search_url = 'https://www.drugbank.ca/unearth/q'
    output = []


    for input_var in farmacos:
        farmaco_output = {}
        farmaco_output['buscado'] = input_var

        api.log('search: '+input_var)
        search_params = {
            'utf8':'✓',
            'searcher':'drugs',
            'query': input_var
        }

        page = api.get(search_url, search_params)

        url = getUrl(api, base_url, page)
        article = api.get(url) if url else page
        url = api.response.url
    
        if article:
            data = []
            name = article.find('h1').text.strip()
            table = article.find('table', {'id': 'drug-moldb-properties'})
            farmaco_output['encontrado'] = name
            farmaco_output['url'] = url
            farmaco_output['propriedades'] = []
            if table:
                check = getattr(table, "find_all", None)
                if callable(check):
                    for row in table.find_all('tr'):
                        cols = row.find_all('td')
                        cols = [val for val in cols]
                        data.append([val for val in cols])

                api.debug('Response sample: %s' % str(data)[:30])

                for propriedade in propriedades:
                    propriedade_output = {}
                    propriedade_output['buscada'] = propriedade
                    propriedade_output['encontradas'] = []
                    for record in data:
                        if len(record) > 0:
                            if propriedade.lower() in record[0].text.strip().lower():
                                link = record[2].find('a', href=True)
                                if link:
                                    fonte = link['href']
                                else:
                                    fonte = record[2].text.strip()
                                propriedade_output['encontradas'].append({
                                    'propriedade': record[0].text.strip(),
                                    'valor': record[1].text.strip(),
                                    'fonte': fonte
                                })
                    farmaco_output['propriedades'].append(propriedade_output)
        output.append(farmaco_output)
    api.save_json(output)
    dt = toDataSheet(output)
    api.save_csv(dt)



def getUrl(api, base_url, page):
    '''
    Retorna url do primeiro link válido, em caso de resultado ambíguo
    '''
    api.log('Page reached: %s' % page.title.text)
    condition = 'Approved'
    articles = page.find_all('div', {'class': 'search-result'})
    for a in articles:
        groups = a.find('div', {'class', 'hit-groups'})

        med = a.find('h2').find('a')
        name = med.text
        url = base_url + med['href']

        if (len(groups.find_all('div')) != 1) or (groups.find('div').text.lower() != condition.lower()):
            api.log('-> Ignoring %s (doesn\'t match conditions)' % name)
        else:
            return url

import pandas as pd
from collections import OrderedDict
def toDataSheet(output):
    data_tmp = []
    for farmaco in output:
        linha = OrderedDict()
        linha['buscado'] = farmaco['buscado']
        linha['encontrado'] = farmaco['encontrado']
        linha['url'] = farmaco['url']
        for propriedade in farmaco['propriedades']:
            if len(propriedade['encontradas']) > 0:
                for found in propriedade['encontradas']:
                    linha[found['propriedade']] = found['valor']
                    linha['fonte ('+found['propriedade']+')'] = found['fonte']
            else:
                linha[propriedade['buscada']] = None
        data_tmp.append(linha)
    return pd.DataFrame(data_tmp)
