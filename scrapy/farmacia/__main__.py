import sys
import argparse
import textwrap
import scrapy
from scrapy import spiderloader
import farmacia.settings
import importlib
from scrapy.crawler import CrawlerProcess

settings = scrapy.settings.Settings(farmacia.settings.__dict__)
spider_loader = spiderloader.SpiderLoader.from_settings(settings)
spiders = spider_loader.list()

parser = argparse.ArgumentParser(description='farmacia web scraper', formatter_class=argparse.RawDescriptionHelpFormatter,
epilog='''
Exemplos de uso:

python farmacia drugbank entradas\drugbank.json
python farmacia drugbank entradas\drugbank.json --tipo=json
python farmacia drugbank entradas\drugbank.json --tipo=json --tipo=csv
python farmacia drugbank entradas\drugbank.json --saida=resultado-drugbank --tipo=json

''')
parser.add_argument('site', choices=spiders)
parser.add_argument('configfile', type=argparse.FileType('r'),
    help="Arquivo de configuração formato json com as configurações específicas para cada site"
)
parser.add_argument('--tipo', action="append", default=[], choices=['csv','json'],
    help="Tipo de saída *multiplo {csv, json}. Default = csv"
)
parser.add_argument('--saida',
    help="Nome do arquivo que será gerado com os resultados. Default = $(nome do site).csv"
)

args = parser.parse_args()

args.configfile.close()
saida = args.saida or args.site

tipo = args.tipo or ['csv']

spider = spider_loader.load(args.site)

c = CrawlerProcess(
    farmacia.settings.__dict__
)
c.crawl(spider, usersettings=args.configfile.name, outputfile=saida, tipo=tipo)
c.start()
