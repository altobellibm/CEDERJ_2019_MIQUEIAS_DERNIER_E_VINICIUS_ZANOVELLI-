from scraping import engine as microframework
from sources.drugbank import drugbank
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)


class Pharmaceutical(microframework.Bot):
    @microframework.trigger('drugbank')
    def drugbank(self, api):
        return drugbank(api, settings)


scraper = Pharmaceutical(dict(
    charset='utf-8',
    parser='html5lib',  # html5lib | lxml | html.parser
    filesystem=dict(
        sources='./sources/',
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
    try:
        fontes = settings['fontes']
    except KeyError:
        scraper.log('Erro! chave \'fontes\' não encontrada')
        raise KeyError
    if 'drugbank' in fontes:
        scraper.drugbank()


