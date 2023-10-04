import os
import csv
from dataprocess import format, souped


#this class contains infomation of temperature for a certain city

class City():

    #initialization City class
    def __init__(self, name, url):

        self.name = name
        self.url = url
        self.info_dict = {}

        #the list of date
        self.date = None
        #list of high/low temperature
        self.temp = None
        #list of high temperature and low temperautre
        self.hightemp, self.lowtemp = None, None




    #fetch 15d weather forcast of city
    #output: dict of highest and lowest temperature by key 'date'
    #format: {date: (high, low), ...}
    def fetch_15d_forecast(self):

        #fetch 7d forcast
        soup = souped(self.url)
        ul = soup.find(attrs={'class': 't clearfix'})
        
        for li in ul.find_all('li'):
            date = li.find('h1').text
            tem = li.find(attrs={'class': 'tem'})
            try: 
                high, low = [format(i) for i in tem.text.split('/')]
            except:
                high = low = format(tem.text)
            
            self.info_dict[date] = (high, low)

    
        #fetch 8-15d forcast
        #as for the 8-15d forcast is in another page, we should reshape url to
        #get new data
        new_city_url = self.url.replace('/weather', '/weather15d')
        soup = souped(new_city_url)
        ul = soup.find(attrs={'class': 't clearfix'})
        
        for li in ul.find_all('li'):
            date = li.find(attrs={'class': 'time'}).text
            #normalize date format
            weekday, day = date[:-1].split('（')
            date = day + '（' + weekday + '）'

            tem = li.find(attrs={'class': 'tem'})
            high, low = [format(i) for i in tem.text.split('/')]
            self.info_dict[date] = (high, low)

        #process the temperature data
        self.date = list(self.info_dict.keys())
        self.temp = list(self.info_dict.values())
        self.hightemp, self.lowtemp = zip(*self.temp)

        return self.info_dict


    #save the data to the filepath in the format of csv
    def save(self, folderpath=os.getcwd()):

        filename_suffix = '温度数据.csv'

        #if there is no exisiting filepath, this folder will be created
        #to save csv files
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
        
        filename = self.name + filename_suffix
        filepath = folderpath + filename
        with open(filepath, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date', 'temperature', 'hightemp', 'lowtemp'])
            writer.writerows(zip(self.date, self.temp, self.hightemp, self.lowtemp))
    
            print("file '%s' created." % filename)