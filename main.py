# -*- coding: utf-8 -*-
"""


@author: Sebastian
"""

from Bibtex_Manager import Bibtex_Manager

#the code given in the main() method can be used as a best practice example
  
def main():
    
    folder_path = r'C:\Users\Sebastian\OneDrive - Hochschule Furtwangen\Desktop\Bibtex-Dokumente' 
    bibfile_path = r'C:\Users\Sebastian\OneDrive - Hochschule Furtwangen\Desktop\Projektarbeit\testfile.bib'
    
    #folder_found_path = r'**********Hier den Pfad zum Ordner in den die PDFs verschoben werden sollen angeben*******'
    
    manager = Bibtex_Manager(folder_path,bibfile_path)
   # manager.extract_from_folder()
    manager.extract_from_file('C:\Users\Sebastian\OneDrive - Hochschule Furtwangen\Desktop\Projektarbeit resourcen\pdfs\3521.full')
if __name__ == '__main__':
    main()
   


 