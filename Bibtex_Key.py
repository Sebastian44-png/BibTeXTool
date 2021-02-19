# -*- coding: utf-8 -*-
"""


@author: Sebastian

"""

import calendar

#structures the retrieved data.
#provides functionlity to create a BibTex entry

class Bibtex_Key:
    
    def __init__(self,data):

#this list represents BibTex entry Types.
#If those attributes are returned from DOI content negotiation, they are includet in the key
#This list can be modified if different entry types are needed
        
        self.search_criteria = ['doi','DOI','url','URL',
                        'created','year','month','publisher','volume',
                        'number','pages','page','author',
                        'title','journal','abstract',
                        'keys','subject']
        

        self.entries = {}
        self.year = ''
        self.source = None
        self.first_author = ''
        
        self.create_entries_from_json(data)
       
# looks up all the entry_critery values in the retrieved json data.
# creates the data for the Bibtex entries
        
    def create_entries_from_json(self,data):
        
        self.source = data.get('source')
        self.first_author = data.get('author')[0]['family']
     
        
        for key in self.search_criteria:
            entry = data.get(key)
            
            if entry != None:
                
                if key == 'created':
                    date_parts = entry['date-parts'][0]
                    
                    self.year = date_parts[0]
                    self.entries['year'] = self.year
                    self.entries['month'] = calendar.month_abbr[date_parts[1]]
                    
                elif key == 'author':
                    shorten_authors = []
               
                    for author in data['author']:
                        shorten_authors.append(author['given'] + ' '+ author['family'])
                       
                    self.entries[key] = shorten_authors
                else:
                    self.entries[key] = entry             
    
# This Methode creates a String, that is formatted in the BibTex style
    def parse_to_string(self):
        
        bibstring = '@article{'+ self.first_author + '_' + str(self.year) +',\n '
        for key in self.entries:
            
            if type(self.entries[key]) == list:
                list_string = ''
                
                for entry in self.entries[key]:
                    
                    list_string = list_string + entry + ', '
                    
                bibstring = bibstring +  str(key) + ' = {'  + list_string + '},' + '\n ' 
                 
            else:
                bibstring = bibstring +  str(key) + ' = {' + str(self.entries[key]) + '},' + '\n '
        
        bibstring = bibstring + '}'
        return bibstring
    
# This Method adds entries to the entries dictionary
    def add_entry(self,key,value):
        
        self.entries[key] = value

