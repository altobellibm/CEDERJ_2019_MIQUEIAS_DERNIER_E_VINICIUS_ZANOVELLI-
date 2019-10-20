from scraping import engine as microframework
from input.drugbank import drugbank

settings = {
    'fontes': {
        'drugbank': {
            'farmacos': [
                'tylenol',
                'ab',
                'Atorvastatin',
                'N-acetyltyrosine',
                'Tannic acid',
                'Fenofibric acid',
                'Calcium glubionate',
                'Ensulizole',
                'Phenoxyethanol',
            ],
            'propriedades': [
                'solubility',
                'density',
                'area',
            ]
        }
    }
}



class Pharmaceutical(microframework.Bot):
    @microframework.trigger('drugbank')
    def drugbank(self, api):
        return drugbank(api, settings)


scraper = Pharmaceutical(dict(
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
    try:
        fontes = settings['fontes']
    except KeyError:
        scraper.log('Erro! chave \'fontes\' não encontrada')
        raise KeyError
    if 'drugbank' in fontes:
        scraper.drugbank()


