import os
import csv
from pyecharts.charts import Map, Timeline, Grid
from pyecharts import options as opts
from dataprocess import format, souped
import webbrowser


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
        #map chart initialization
        self.map_chart = Map(init_opts=opts.InitOpts(width="1000px", height="600px", theme='white'))
        self.map_chart.set_global_opts(
                title_opts=opts.TitleOpts(
                    title="%s省15天温度预报图" % self.name,
                    pos_top="2%",
                    pos_left="2%",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=24,color="#1f1e33")
                ),
                legend_opts=opts.LegendOpts(is_show=True, pos_top="40px", pos_right="30px"),
                tooltip_opts=opts.TooltipOpts(
                    is_show=True,
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_calculable=True,
                    pos_left="5%",
                    pos_top="center",
                    min_=10,
                    max_=35,
                ),
            )


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
        


    
    #return date list
    def datelist(self):

        return self.cities[0].date


    #get city high temperature information in one day
    #output:a list of name and temperature
    #format:[(name, temperature), ...]
    def hightemplist(self, date):
        
        hightemp_list = list()
        for city in self.cities:
            index = city.date.index(date)
            hightemp_list.append((city.name, city.hightemp[index]))

        return hightemp_list


    #get city low temperature information in one day
    #output:a list of name and temperature
    #format:[(name, temperature), ...]
    def lowtemplist(self, date):
        
        lowtemp_list = list()
        for city in self.cities:
            index = city.date.index(date)
            lowtemp_list.append((city.name, city.lowtemp[index]))

        return lowtemp_list


    #add a map chart of temperature
    def add_map_chart(self, datalist, series_name=""):

        self.map_chart.add(
            series_name=series_name,
            data_pair=datalist,
            maptype=self.name,
            zoom=1,
            is_map_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=True),
        )


    #reinitialize map chart
    def readd_map_chart(self, datalist, series_name=""):

        self.map_chart = (
            Map(init_opts=opts.InitOpts(width="1000px", height="600px", theme='white'))
            .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="%s省15天温度预报图" % self.name,
                        pos_top="2%",
                        pos_left="2%",
                        title_textstyle_opts=opts.TextStyleOpts(font_size=24,color="#1f1e33")
                    ),
                    legend_opts=opts.LegendOpts(is_show=True, pos_top="40px", pos_right="30px"),
                    tooltip_opts=opts.TooltipOpts(
                        is_show=True,
                    ),
                    visualmap_opts=opts.VisualMapOpts(
                        is_calculable=True,
                        pos_left="5%",
                        pos_top="center",
                        min_=10,
                        max_=35,
                    ),
                )
        )

        self.add_map_chart(datalist, series_name)


    #show the timeline map of temperature of province
    def show(self): 
        
        #setup the timeline
        timeline = Timeline(init_opts=opts.InitOpts(width="1400px", height="600px"))
        series_name = "最高温度"

        for date in self.datelist():
            #add temperature map for date
            self.readd_map_chart(self.hightemplist(date), series_name)

            timeline.add(self.map_chart, date)
            timeline.add_schema(
            is_timeline_show=True,
            is_auto_play=False,
            is_inverse=False,
            play_interval=1500,
            pos_left="center",
            pos_right="right",
            pos_bottom='2%',
            is_loop_play=False
            )

        html_name = "%s省%s地图.html" % (self.name, series_name)
        timeline.render(html_name)

        webbrowser.open(html_name)

