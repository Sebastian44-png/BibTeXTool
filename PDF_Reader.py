# -*- coding: utf-8 -*-
"""


@author: Sebastian
"""
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from PyPDF2 import PdfFileReader
import io
import re


class PDF_Reader:
    
    def __init__(self,file):
        
        self.file = file
    
    
    def extract_page(self,page_no):
    
        # Supply the password for initialization.
        password = ''
        codec = 'utf-8'
        retstr = io.StringIO()
        laparams = LAParams()
        
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(self.file)
        
        # Create a PDF document object that stores the document structure.
        document = PDFDocument(parser, password)
        
        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
            
        # Create a PDF resource manager object that stores shared resources.   
        rsrcmgr = PDFResourceManager()
        
        # Create a PDF device object.
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        # Create PDF pages
        page = list(PDFPage.create_pages(document))
        
        #Process the page thats needed
        interpreter.process_page(page[page_no])
                   
        text = retstr.getvalue()
     
        device.close()
        retstr.close()
        return text
    
    def get_number_of_pages(self):
        
        pdf = PdfFileReader(self.file)
        
        try:
            num_pages = pdf.getNumPages()
        except:
            print('pdf kann nicht gelesen werden')
            return None
        
        return num_pages
  
#Methode looks for a DOI in a String(representing the PDF page)
#If DOI was found its returned, otherwise the return value equals None
    def search_doi(text):
        
            #compiling a regular expression, that can be used for pattern matching
            pattern = re.compile('10[.]\d*[/][^\s><#]*')
            
            #matching the pattern with the text of the page
            doi_spec = pattern.search(text)
        
            if doi_spec != None:
                #eliminating line breaks
                doi = re.sub('\n','',doi_spec.group())
                
                if(len(doi)>100):
                    return None
                
                return doi
            else:
                return None
            

       
    
