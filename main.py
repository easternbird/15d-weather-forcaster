import os
from datafetch import get_data_and_save
from city import Province

if __name__ == '__main__':

    folderpath = os.getcwd() + '\\data\\'
    province_name = '安徽'

    #get temperature data and save to csv files
    get_data_and_save(province_name, folderpath)
    #setup an empty Province class
    province = Province(province_name)
    #load the city infomation in csv files
    province.csv_add_all(folderpath)
    #show data infomation of province
    province.show()
