# -*- coding: utf-8 -*-

import scrapy
import json
import math


class News112Spider(scrapy.Spider):
    name = 'grec'
    start_urls = ['https://diavgeia.gov.gr/luminapi/api/search?page=0&q=decisionType:'
                  '%22%CE%A0%CE%A1%CE%91%CE%9E%CE%95%CE%99%CE%A3+%CE%A7'
                  '%CE%A9%CE%A1%CE%9F%CE%A4%CE%91%CE%9E%CE%99%CE%9A%CE%9F%CE%A5+-'
                  '+%CE%A0%CE%9F%CE%9B%CE%95%CE%9F%CE%94%CE%9F%CE%9C%CE%99%C'
                  'E%9A%CE%9F%CE%A5+%CE%A0%CE%95%CE%A1%CE%99%CE%95%CE%A7%CE%9'
                  'F%CE%9C%CE%95%CE%9D%CE%9F%CE%A5%22&sort=recent']
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_LEVEL': 'INFO'
    }
    headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78',
               }
    # data_final = pd.read_csv('final_full2.csv', usecols=[ 'ΑΔΑ' ])
    # save_data = set(data_final['ΑΔΑ'].values.tolist())

    def parse(self, response, **kwargs):
        page = math.ceil((json.loads(response.text)['info']['total'])/
                         (json.loads(response.text)['info']['actualSize']))

        for i in range(0, int(page)):
            link = f'https://diavgeia.gov.gr/luminapi/api/search?page={i}&q=decisionType:' \
                   f'%22%CE%A0%CE%A1%CE%91%CE%9E%CE%95%CE%99%CE%A3+%CE%A7%CE%A9' \
                   f'%CE%A1%CE%9F%CE%A4%CE%91%CE%9E%CE%99%CE%9A%CE%9F%CE%A5+-' \
                   f'+%CE%A0%CE%9F%CE%9B%CE%95%CE%9F%CE%94%CE%9F%CE%9C%CE%99%CE%9A%CE%9F%C' \
                   f'E%A5+%CE%A0%CE%95%CE%A1%CE%99%CE%95%CE%A7%CE%9F%CE%9C%CE%95%CE%9D%CE%9F%CE%A5%22&sort=recent'
            yield scrapy.Request(link, callback=self.read_data, headers=self.headers)

    def read_data(self, response):
        text = json.loads(response.text)
        for i in range(len(text['decisions'])):
            link=text['decisions'][i]['ada']
            # if  link not in self.save_data:
            full_link = f'https://diavgeia.gov.gr/luminapi/api/decisions/view/{link}'
            yield scrapy.Request(url=full_link, callback=self.api_text, headers=self.headers)

    def api_text(self, response):
        text = json.loads(response.text)
        data = {
            'ΑΔΑ': text['ada'],
            'Κατάσταση': text['status'],
            'Ημερομηνία ανάρτησης': text['publishTimestamp'],
            'Τελευταία τροποποίηση': text['submissionTimestamp'],
            'Ηλεκτρονικό αρχείο': text['documentUrl'],
            'Είδος': text['meta'][0]['Είδος'],
            'Θέμα': text['meta'][1]['Θέμα'],
            'Θεματικές κατηγορίες': None if text['meta'][2] == {} else text['meta'][2],
            'Αρ. πρωτοκόλλου': text['meta'][3]['Αρ. πρωτοκόλλου'],
            'Ημερομηνία έκδοσης': text['meta'][4]['Ημερομηνία έκδοσης'],
            'Φορέας': text['meta'][5]['Φορέας'],
            'Οργανωτικές Μονάδες': text['meta'][6]['Οργανωτικές Μονάδες'],
            'Υπογράφοντες': text['meta'][7]['Υπογράφοντες'],
            'Τύπος Πράξης': text['meta'][8]['Τύπος Πράξης'],
            'Γεωγραφική Περιοχή': text['meta'][9]['Γεωγραφική Περιοχή'] ,
        }
        print(data)
        yield data
