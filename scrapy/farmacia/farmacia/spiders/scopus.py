# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
import bs4 as bs
import json
import requests

from ..utils import SettingsSpyder

class ScopusSpider(SettingsSpyder):
    name = 'scopus'

    def start_requests(self):
        yield scrapy.Request(url='https://scopus.com/', callback=self.generateCookie, dont_filter=True)
    def generateCookie(self, response):
        count = self.user_settings['count']
        search = self.user_settings['busca']
        apiKey = self.user_settings['api-key']

        search_url = 'https://api.elsevier.com/content/search/scopus?'

        self.headers = {
            'X-ELS-APIKey': apiKey,
            'Accept': '*/*'
        }

        params = {
            'query': search,
            'count': count,
        }

        url = search_url+urllib.parse.urlencode(params)

        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_search)
    def parse_search(self, response):
        try:
            result = json.loads(response.text)['search-results']['entry']
        except KeyError:
            result = []

        for artigo in result:
            params = {
                'httpAccept': 'application/json',
                'fields': 'description'
            }

            meta = {
                'item': artigo
            }
            links = {'link:'+a['@ref']: a['@href'] for a in artigo['link']}
            artigo.update(links)
            artigo.pop('link',None)
            artigo.pop('link:author-affiliation',None)
            artigo.pop('link:self',None)
            artigo.pop('@_fa',None)

            doc_details_url = artigo['prism:url']+'?'+urllib.parse.urlencode(params)

            yield scrapy.Request(url=doc_details_url, headers=self.headers, callback=self.parse_doc_details, meta=meta)
            
    def parse_doc_details(self, response):
        item = response.meta['item']
        obj = json.loads(response.text)
        try:
            link = obj['abstracts-retrieval-response']['item']['bibrecord']['head']['source']['website']\
                ['ce:e-address']['$']
        except:
            link = None
        item['source-address'] = link
        try:
            abstract = obj['abstracts-retrieval-response']['item']['bibrecord']['head']['abstracts']
        except:
            abstract = None
        item['abstract'] = abstract
        srcView = None
        try:
            r = requests.get('https://doi.org/'+item['prism:doi'], allow_redirects=False)
            if r.status_code == 302:
                srcView = str(r.headers['Location'])
        except:
            srcView = None
        item['view-in-source'] = srcView
        


        meta = {
            'item': item,
            }

        url_source_details = 'https://www.scopus.com/source/citescore/{}.uri'.format(item['source-id'])
        headers = {
            'Accept': 'application/json',
            'referer': url_source_details
        }

        yield scrapy.Request(url=url_source_details, headers=headers, callback=self.parse_source_details, meta=meta,dont_filter=True)

    def parse_source_details(self, response):
        try:
            obj = json.loads(response.text)
            score = [m['rp'] for m in obj['yearInfo'][obj['lastYear']]['metricType'] if m['documentType']=='all']
            score = score[0]
        except:
            score = 0
        response.meta['item']['source-score'] = score
        yield response.meta['item']