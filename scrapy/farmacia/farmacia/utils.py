import scrapy
import json

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            for a in x:
                flatten(a, name + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

class SettingsSpyder(scrapy.spiders.Spider):
    def __init__(self,*args,usersettings='',outputfile='',tipo=['json'],**kwargs):
        self.user_settings = {}
        self.outputfile = outputfile
        self.tipo = tipo
        if(usersettings):
            with open(usersettings,encoding="utf-8") as json_file:
                data = json.load(json_file)
                self.user_settings = data
        super().__init__(*args, **kwargs)
