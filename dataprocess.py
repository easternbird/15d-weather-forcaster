import requests
from bs4 import BeautifulSoup


#return soup of an url after request
#input:url
#output:soup of a html
def souped(url, headers=None):

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text

    soup = BeautifulSoup(html, features='lxml')
    return soup


#convert the data with unit into int type
def format(data):

    formatted_data = None
    
    try:
        formatted_data = int(data)
    except:
        
        if len(data) > 0:
            for i in range(1, len(data)):
                try:
                    formatted_data = int(data[:-i])
                    break
                except:
                    pass

    return formatted_data