# Files to import (name.basics.tsv, title.basics.tsv)
# should be in the same path as import_tsv.py script.
# """

import csv
import os
import requests
import re
from zipfile import ZipFile 

# url='https://datasets.imdbws.com/name.basics.tsv.gz'
# r = requests.get(url, allow_redirects=True)
# #open('name.basics.tsv.gz', 'wb').write(r.content)

# # specifying the zip file name 
# file_name = "name.basics.tsv.gz"
  
# # opening the zip file in READ mode 
# with ZipFile(file_name, 'r') as zip: 
#     # printing all the contents of the zip file 
#     zip.printdir() 
  
#     # extracting all the files 
#     print('Extracting all the files now...') 
#     zip.extractall() 
#     print('Done!') 

with open("name.basics.tsv", 'r',encoding='utf-8') as myfile:
  with open("name.basics.csv", 'w',encoding='utf-8') as csv_file:
    for line in myfile:
      fileContent = re.sub("\t", ",", line)
      csv_file.write(fileContent)
csv_file.close()