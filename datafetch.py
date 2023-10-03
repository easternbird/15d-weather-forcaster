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


#fetch the list of weather forcast url for every city in Anhui
#input: the html of website
#output: a list of package with city name and its own url
#format:[(city, url), ...]
def fetch_url_list(url, headers=None):
    
    soup = souped(url, headers=headers)
    #find all weather forcast websites for every city and pack them
    url_list = []
    for dl in soup.find(id='forecastID'):
        dt = dl.find('dt')
        try:
            #get city name and reshape
            city = dt.a['title']
            city = city[:-4] + '市'
            #get url name
            city_url = dt.a['href']
            #city_url = city_url.replace('/weather', '/weather15d')
            url_list.append((city, city_url))
        except:
            pass

    return url_list
    

#fetch 15d weather forcast of city
#input:url of city
#output: dict of highest and lowest temperature by key 'date'
#format: {date: (high, low), ...}
def fetch_15d_forecast(city_url):

    city_dict = {}

    #fetch 7d forcast
    soup = souped(city_url)
    ul = soup.find(attrs={'class': 't clearfix'})
    
    for li in ul.find_all('li'):
        date = li.find('h1').text
        tem = li.find(attrs={'class': 'tem'})
        try: 
            high, low = [int(i) for i in tem.text[:-2].split('/')]
        except:
            try:
                high = low = int(tem.text[:-2])
            except:
                high, low = [int(i[:-2]) for i in tem.text.split('/')]
        city_dict[date] = (high, low)

    #fetch 8-15d forcast
    #as for the 8-15d forcast is in another page, we should reshape url to
    #get new data
    city_url = city_url.replace('/weather', '/weather15d')
    soup = souped(city_url)
    ul = soup.find(attrs={'class': 't clearfix'})
    
    for li in ul.find_all('li'):
        date = li.find(attrs={'class': 'time'}).text
        #normalize date format
        weekday, day = date[:-1].split('（')
        date = day + '（' + weekday + '）'

        tem = li.find(attrs={'class': 'tem'})
        high, low = [int(i[:-1]) for i in tem.text.split('/')]
        city_dict[date] = (high, low)

    # print(city_dict)

    return city_dict


#return 15d weather forcast for city in url_list
#input: url_list
#output:dict of temperature forcast
#format: {city: _15d_forcast_dict, ...}
def fetch_15d_forcast_dict(url_list):
    
    forcast_dict = {}

    for city, url in url_list:
        print(city, url)
        _15d_forecast_dict = fetch_15d_forecast(url)
        forcast_dict[city] = _15d_forecast_dict

    print(forcast_dict)
