import ttkbootstrap as ttk
from ttkbootstrap.constants import *



province_list = ['安徽', '北京', '福建', '甘肃', '广东', 
                 '广西', '贵州', '海南', '河北', '河南', 
                 '黑龙江', '湖北', '湖南', '吉林', '江苏', 
                 '江西', '辽宁', '内蒙古', '宁夏', '青海', 
                 '山东', '山西', '陕西', '四川', '天津', 
                 '西藏', '新疆', '云南', '浙江']



#this class shows the main window for program
class MyWindow():

    #initialization
    def __init__(self, title):
        
        self.title = title
        self.root = ttk.Window(title=title)

        #button list
        self.buttons : list[ttk.Button] = []

        #combobox
        self.combobox : ttk.Combobox = None

        #calculate the center position of window
        x = int((self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2)
        y = int((self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2)

        #center the window
        self.root.geometry("+{}+{}".format(x, y))


    #show message on main window
    def show_message(self, text, row=None, column=None):

        if self.root:
            message = ttk.Label(self.root, text=text)
            message.grid(row=row, column=column)




    def add_message(self, text, row=None, column=None, padx=None, pady=None):
        #set text and combobox
        message = ttk.Label(self.root, text=text)
        message.grid(row=row, column=column, padx=padx, pady=pady)


    
    def add_combobox(self, row=None, column=None, columnspan=None, padx=None, pady=None):
        self.combobox = ttk.Combobox(
                    master=self.root,
                    bootstyle = DANGER,
                    font=("微软雅黑", 10),
                    values=province_list,
                )
        #show the value which index refers to first
        self.combobox.current(1)
        self.combobox.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)

    

    def add_button(self, text, row=None, column=None, columnspan=None, padx=None, pady=None, command=None):

        #initialize button
        button = ttk.Button(self.root, text=text, bootstyle=(PRIMARY, "outline-toolbutton"), command=command)
        button.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)

        self.buttons.append(button)

        #return index of button
        return self.buttons.index(button)
    

    #start window mainloop
    def start(self):

        self.root.mainloop()


    #quit the mainloop
    def quit(self):
        
        self.root.quit()

