import os
from datafetch import get_data_and_save
from city import Province

if __name__ == '__main__':

    folderpath = os.getcwd() + '\\data\\'
    #get temperature data and save to csv files
    get_data_and_save(folderpath)
    #setup an empty Province class
    Anhui = Province('安徽')
    #load the city infomation in csv files
    Anhui.csv_add_all(folderpath)
    #show data infomation of province
    Anhui.show()
    for city in Anhui.cities:
        print(city.name, city.temp, city.hightemp, city.lowtemp)


