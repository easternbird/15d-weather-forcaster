import requests
from bs4 import BeautifulSoup


region_list = ['北京', '重庆', '上海', '天津', ]


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


#this function return total name of a province/district
def total_name(name):
    suffix = ''
    if name in region_list:
        suffix = '市'
    else:
        suffix = '省'

    return name + suffix




#this function return region suffix of a province/district
def suffix(name):
    suffix = ''
    if name in region_list:
        suffix = '区'
    else:
        suffix = '市'

    return suffix