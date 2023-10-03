from datafetch import fetch_url_list, get_city_list
from city import City

url = 'http://www.weather.com.cn/html/province/anhui.shtml'
url_list = fetch_url_list(url)
city_list = get_city_list(url_list)

# print(list(city_dict['合肥市'].values()))

for city in city_list:
    print(city.name, city.hightemp)
    print(city.name, city.lowtemp)