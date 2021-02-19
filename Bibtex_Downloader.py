# -*- coding: utf-8 -*-
"""


@author: Sebastian
"""

import urllib.request

import requests

 # downloads a Bibtex Key from a DOI

class Bibtex_Downloader:
   
    def __init__(self):  
        self.status = 0
       
#Content negotiated requests        
# the method redirects to a metadata service hosted by the DOI's registration agency.--> CrossRef, DataCite and mEDRA        
#returned format is cls-json
        
    def get_json_metadata(self,doi, cache={}):
   
        if doi in cache:
            return cache[doi]
        
        url = 'https://doi.org/' + urllib.request.quote(doi)
        header = {
            'Accept': 'application/vnd.citationstyles.csl+json;q=1.0',
        }
        response = requests.get(url, headers=header)
        data = response.json()
        self.status = response.status_code
        
        if response:
            cache[doi] = data
        
        if(response.status_code == requests.codes.ok):
            
            return data
        else:
            return None
        
manager =Bibtex_Downloader()
jasondata = manager.get_json_metadata(r'10.1073/pnas.1611835114')
print()
