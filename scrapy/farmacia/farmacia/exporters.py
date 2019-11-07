from scrapy import signals
from scrapy.exporters import PythonItemExporter, CsvItemExporter
import pandas as pd
import json

from .utils import flatten_json

class JSONExporter(PythonItemExporter):
    def __init__(self, file_name):
        self.file_name = file_name
    def start_exporting(self):
        self.data = []
        self.file = open(self.file_name, 'w', encoding='utf-8')
        self.file.write(json.dumps(self.data))
    def export_item(self,item):
        self.data.append(item)
        self.file.truncate(0)
        self.file.seek(0)
        self.file.write(json.dumps(self.data))
    def finish_exporting(self):
        self.file.close()

class CSVExporter(PythonItemExporter):
    def __init__(self, file_name):
        self.file_name = file_name
    def start_exporting(self):
        self.data = []
    def export_item(self,item):
        item = {k.encode('cp1252', errors='ignore').decode('cp1252', errors='ignore'): 
            v.encode('cp1252', errors='ignore').decode('cp1252', errors='ignore') for k, v in item.items()}

        self.data.append(item)
    def finish_exporting(self):
        data = pd.DataFrame(self.data)
        data.to_csv(self.file_name, sep=';', index=False, encoding='cp1252' )


class JSONExportPipeline(object):
    tipo = 'json'
    exporter_class = JSONExporter
    def __init__(self):
        self.files = {}

    def open_spider(self, spider):
        if self.tipo in spider.tipo:
            file_name =  getattr(spider, 'outputfile', '').strip() or spider.name
            if file_name.lower()[-(len(self.tipo)+1):] != self.tipo:
                file_name += '.'+self.tipo
            self.files[spider] = file_name
            self.exporter = self.exporter_class(file_name)
            self.exporter.start_exporting()

    def close_spider(self, spider):
        if self.tipo in spider.tipo:
            file_name = self.files.pop(spider)
            self.exporter.finish_exporting()

    def process_item(self, item, spider):
        if self.tipo in spider.tipo:
            self.exporter.export_item(item)
        return item


class CSVExportPipeline(JSONExportPipeline):
    tipo = 'csv'
    exporter_class = CSVExporter
    def process_item(self, item, spider):
        if self.tipo in spider.tipo:
            self.exporter.export_item(flatten_json(item))
        return item


