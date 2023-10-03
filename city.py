#this class contains infomation of temperature for a certain city

class City():

    #initialization City class
    def __init__(self, name, info_dict):

        self.name = name
        self.info_dict = info_dict

        #the list of date
        self.date = list(self.info_dict.keys())
        #list of high/low temperature
        self.temp = list(self.info_dict.values())
        #list of high temperature and low temperautre
        self.hightemp, self.lowtemp = zip(*self.temp)