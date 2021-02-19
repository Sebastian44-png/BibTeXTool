# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:50:14 2019

@author: Sebastian
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 19:30:27 2019

@author: Sebastian
"""

from PDF_Reader import PDF_Reader
from Bibtex_Downloader import Bibtex_Downloader
from Bibtex_Key import Bibtex_Key
from pathlib import Path
import shutil
import os

class Bibtex_Manager:
    
    def __init__(self,pdf_folder_path, bibfile_path, found_folder_path = None , maximum_pages_to_search = 8, absolute_links = True):
        
        self.bibfile_path = Path(bibfile_path)
        self.pdf_folder = Path(pdf_folder_path)
        self.default_folder_found = self.pdf_folder / 'key_found'
        self.absolute_links = absolute_links
        
        if(found_folder_path != None):
            self.folder_found = Path(found_folder_path)
        else:
            self.folder_found = self.default_folder_found
                
        self.result = {'num_of_files_searched' : 0,
                       'num_success' :0,} 
        self.maximum_pages_to_search = maximum_pages_to_search
          
 #extracts the Bibtex-key of a file and writes it to a Bibtex file 
    def extract_from_file(self,file_name):
                
        print('Datei: ' + str(self.pdf_folder / file_name) + '\n')
            
        with open(self.pdf_folder / file_name,'rb') as f:
                
            status = self.extract_key(f,file_name)      #status indicates if the extraction was successful
            f.close()
                
        # moves the file depending on the success of the extraction (result in variable status)
        if(status):
            shutil.move(self.pdf_folder / file_name, self.folder_found / file_name)
        else:
            print('failed')
            
# extracts all Bibtekeys from the files of an order path and writes them to a Bibtex file.                
    def extract_from_folder(self):   
        
        self.setup_folders()
        self.result['num_of_files_searched'] = 0
        self.result['num_success'] = 0
      
        file_names = os.listdir(self.pdf_folder)
        
        print('extraction from = '+ str(self.pdf_folder)+ '\n'+ '     ' + 'num_file_names =' + str(len(file_names)) + '\n')
        
        for file_name in file_names:
            
            if not os.path.isfile(self.pdf_folder / file_name):
                continue
            
            self.result['num_of_files_searched'] += 1
            print('Datei: ' + str(self.pdf_folder / file_name) + '\n')
            
            with open(self.pdf_folder / file_name,'rb') as f:
                
                status = self.extract_key(f,file_name)         #status indicates if extraction was successful
                f.close()
                
             # moves the file depending on the success of the extraction (result in variable status)
            if(status):
        
                shutil.move(self.pdf_folder / file_name, self.folder_found / file_name)
                self.result['num_success'] += 1
                
            print( str(self.result['num_success']) + ' / ' + str(self.result['num_of_files_searched']))
            print('***************************************************')
                  
        
# extracts the bibtexkey of a PDF file, and writes it to a .bib file.                   
    def extract_key(self,pdf_file,file_name):
    
        reader = PDF_Reader(pdf_file)
        
        # only the first pages of the PDF document should be searched, the first 20 % + 1 will be searched.
        # it can be defined how many pages should be searched at most
        num_pages = reader.get_number_of_pages()
        if num_pages != None:
            num_pages_to_extract = int(num_pages * 0.2) + 1
        else:
            num_pages_to_extract = 0
       
        doi = None
        for i in range(num_pages_to_extract):
            
            print('page: ' + str(i) + '...')
            # extraktion of page numer i
            try:
                pdf_page = PDF_Reader.extract_page(reader,i)
            except:
                print("page extraction failed")
            # using regular expressions, searches for the DOI in page i
            else:
                doi = PDF_Reader.search_doi(pdf_page)
            
            if(doi != None or i >= self.maximum_pages_to_search):
                break
                           
    # If DOI was found, load bibtexkey and write to the end of a .bib file             
        if(doi != None):
            
            print('doi: '+ doi)
            Downloader = Bibtex_Downloader()
            
            try:
                json_metadata = Downloader.get_json_metadata(doi)
                Bibkey = Bibtex_Key(json_metadata)
                print('hattp status: ' + str(Downloader.status))
    # Adding a link to the PDF file's entry in the Bibtex key
            except:
                print('download failed')
                return False
            else:      
                self.link_file_to_key(file_name,Bibkey)

                try:
                    if self.print_bibKey(self.bibfile_path, Bibkey) == True:
                        return True 
                    else:
                        return False
                except:
                    print('writing key failed')      
        return False
 # Writes the bibtexkey to the default .bib file    
    def print_bibKey(self,bibfile_path, Bibkey):
       
        with open(bibfile_path,'a') as f:
            if(os.path.getsize(bibfile_path) > 0):
                f.write('\n' + Bibkey.parse_to_string())
                return True
            else:
                f.write(Bibkey.parse_to_string())
                return True

#Set up a folder structure: - One folder for documents found and one for documents not found
#If folder already exists then no new folder will be created 
    def setup_folders(self):
                 
        try:
            if not os.path.exists(self.folder_found):
                os.makedirs(self.default_folder_found)
                self.folder_found = self.default_folder_found
              
        except OSError:
            print ('Error: Creating directory. ' +  str(self.folder_found))
        
#this Methode adds a link, as an entry to the BibtyKey
#The functionlity of the class Bibkey was used for this purpose
    def link_file_to_key(self,file_name,Bibkey):
        
        if(self.absolute_links == True):
            name = str(self.folder_found / file_name)
            link = name.replace('\\','\\\\')
            Bibkey.add_entry('file',link)
        else:
            link = ':' + file_name + ':PDF' 
            Bibkey.add_entry('file',link)
            
