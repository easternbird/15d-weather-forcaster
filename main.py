import os
from utils.datafetch import get_data_and_save
from utils.city import Province
from GUI.show import MyWindow
from ttkbootstrap.constants import *
from threading import Thread

    

if __name__ == '__main__':

    #events to be handled
    #--------------------------------------
    def button_yes(province_name:list, index=0):
        #show tips
        root.show_message("正在获取城市信息")

        #disable button to avoid more clicks
        root.buttons[index].configure(state=DISABLED)

        #get province name
        province_name.append(root.combobox.get())

        #quit the window
        root.quit()


    def button_no():

        root.quit()
    #--------------------------------------

    province_name = []
    folderpath = os.getcwd() + '\\data\\'

    #set up the window
    root = MyWindow(title="15日天气预报查询系统")

    #add message tips
    root.add_message(text="请输入需要查询的省份：", row=0, column=0, padx=10)
    #add combobox
    root.add_combobox(row=0, column=1, columnspan=2, padx=10, pady=10)
    #add buttons
    root.add_button(text="确定", row=2, column=1, pady=10, 
                    command=lambda:Thread(target=button_yes, args=(province_name, )).start())
    root.add_button(text="取消", row=2, column=2, pady=10, command=button_no)

    #start mainloop
    root.start()

    if province_name:
        province_name = province_name[0]
        #get temperature data and save to csv files
        #if you have already saved data, this step can be passed
        get_data_and_save(province_name, folderpath)
        #setup an Province class
        province = Province(province_name)
        #load the city infomation in csv files
        province.csv_add_all(folderpath)
        #show data infomation of province
        province.show()
    
    

