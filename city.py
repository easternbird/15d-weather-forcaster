import os
import csv
from dataprocess import format, souped


#this class contains infomation of temperature for a certain city

class City():

    #initialization City class
    def __init__(self, name, url=None):

        self.name = name
        self.url = url
        self.info_dict = dict()

        #the list of date
        self.date = list()
        #list of high/low temperature
        self.temp = list()
        #list of high temperature and low temperautre
        self.hightemp, self.lowtemp = list(), list()




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
        #for the 8-15d forcast is in another page, we should reshape url to
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




#this class contains cities in a province
class Province():
    
    #initialization
    def __init__(self, name):
        
        #province name
        self.name = name
        #cities list
        self.cities = list()


    #add a new city to the province
    def add(self, city):
        
        self.cities.append(city)


    #add a new city through csv file
    #if the file is not csv or csv with invalid type, this method won't add anything
    def csv_add(self, filepath):
        
        filename = os.path.basename(filepath)
        try:
            city_name = filename[:-8]
            new_city = City(city_name)

            #open csv file
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    new_city.date.append(row['date'])
                    new_city.temp.append(eval(row['temperature']))
                    new_city.hightemp.append(eval(row['hightemp']))
                    new_city.lowtemp.append(eval(row['lowtemp']))

            self.cities.append(new_city)
        except:
            print('Invalid type!')



    #add all cities the filepath contains in csv files
    def csv_add_all(self, filepath):

        filenames = os.listdir(filepath)
        for filename in filenames:
            newpath = filepath + filename
            self.csv_add(newpath)




    #show the data of temperature of province
    def show(self):
        pass