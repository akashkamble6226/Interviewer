import os
import requests

url='https://raw.githubusercontent.com/developerforce/trailhead-files/master/contacts_to_import.csv'
response = requests.get(url)
with open(os.path.join("small_files", "mycsv"), 'wb') as f:
    f.write(response.content)