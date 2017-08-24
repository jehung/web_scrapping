## Goal: get the thread that is top 100 popular: by views, by replies

## Write function to sort by reviews or replies



import requests

res = requests.get('http://www.f150ecoboost.net/forum/42-2015-ford-f150-ecoboost-chat')
res.raise_for_status()  # this line trows an exception if an error on the 
                         # connection to the page occurs. 
print(res.text)