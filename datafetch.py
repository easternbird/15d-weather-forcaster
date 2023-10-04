import os
from dataprocess import souped
from city import City



#fetch the list of weather forcast url for every city in Anhui
#input: the html of website
#output: a list of package with city name and its own url
#format:[(city, url), ...]
def fetch_url_list():
    
    url = 'http://www.weather.com.cn/html/province/anhui.shtml'
    soup = souped(url)
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



#return city list containing 15d temperature info
def get_city_list(url_list):
    
    url_list = fetch_url_list()
    city_list = []
    
    #create the city list
    for cityname, url in url_list:
        newcity = City(cityname, url)
        #fetch the 15d forcast for every city
        newcity.fetch_15d_forecast()
        print('obtaining city: %s' % newcity.name)
        city_list.append(newcity)

    return city_list



#save the data from city list to csv
#input:the list of city class
#output:a csv file, headers: name temperature hightemp lowtemp
def save_to_csvfile(city_list):

    folderpath = os.getcwd() + '\\data\\'

    for city in city_list:
        city.save(folderpath)



#get the temperature data and save to csv files
#input: None
#output:csv files
def get_data_and_save():

    #get data from url
    url_list = fetch_url_list()
    city_list = get_city_list(url_list)
    #save csv files
    save_to_csvfile(city_list)