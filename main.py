import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb


import pandas as pd
import numpy as np

DISTANCE_MATRIX = 'distance_matrix.xlsx'


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        

    def init_main(self):
        
        self.backgr = tk.Frame(root,height=450,bg = '#8cc983')
        self.backgr.pack(side=tk.TOP,fill = tk.X)

        label_entry_city1 = tk.Label(self.backgr, text='Звідки:',bg = '#8cc983')#назва поля введення
        label_entry_city1.place(x=30, y=50)
        
        label_entry_city2 = tk.Label(self.backgr, text='Куди:', bg = '#8cc983')
        label_entry_city2.place(x=30, y=100)

        label_entry_weight = tk.Label(self.backgr, text='Вага вантажу, т',bg = '#8cc983')
        label_entry_weight.place(x=30, y=150)

        label_type_grain = tk.Label(self.backgr, text='Оберіть тип зернової культури',bg = '#8cc983')
        label_type_grain.place(x=30, y=200)

        label_select = tk.Label(self.backgr, text='Додати вартість зберігання зерна на елеваторі',bg = '#8cc983')
        label_select.place(x=30, y=270)

        self.entry_city1 = tk.Entry (self.backgr)#поле вводу
        self.entry_city1.place(x=220, y=50)
        
        self.entry_city2 = tk.Entry(self.backgr)
        self.entry_city2.place(x=220, y=100)

        self.entry_weight = tk.Entry(self.backgr)
        self.entry_weight.place(x=220, y=150)

        self.combobox_type = ttk.Combobox (self.backgr, values = [u'Пшениця', u'Кукурудза', u'Ячмінь',u'Соя'])#випадаючий список
        self.combobox_type.current(0)#значення по дефолту
        self.combobox_type.place(x=220, y=200)

        
        btn_ok = ttk.Button(self.backgr, text='Розрахувати',  command=self.calculator)
        btn_ok.place(x=170, y=350)

        self.add_img = tk.PhotoImage(file="button_add.png")
        btn_open_dialog = tk.Button(self.backgr, text='Додати зберігання ', image=self.add_img,  bg = '#8cc983', command=self.open_dialog)
        btn_open_dialog.place(x=308, y=260)

        label_comment = tk.Label(root, text='''Застереження : Для розрахунку потрібне повне 
        та коректне введення інформації ''')
        label_comment.place(x=70, y=480)
                
        self.focus_set()

    def open_dialog(self):
        Child()
             

    def  check_weight(self):
        
        try:
            self.weight = float(self.entry_weight.get())
        except ValueError:
            mb.showinfo("Number Error","Your weight must be a number!")


    def city_db(self):
        self.excel_data_df = pd.read_excel(DISTANCE_MATRIX,sheet_name='distance')


    def grain_type_index(self):
        self.index_dict = {'Пшениця':0.99,'Кукурудза':0.93,'Ячмінь':0.97,'Cоя':0.90}
     
    
    def distance_between_city(self):
        self.city_db()

        self.point1 = self.entry_city1.get()
        self.point2 = self.entry_city2.get()       
    
        try:
            self.distance = self.excel_data_df.loc[self.excel_data_df['Назва міста'] == self.point1,[self.point2]]
        except KeyError:
            mb.showinfo("Key Error","Incorrect city")


    def distance_tarrifs (self):
            
        if 0 < self.distance.values[0] < 50:
            self.tarrifs=3.47
        elif 50 <= self.distance.values[0] < 100:
            self.tarrifs=2.7
        elif 200 <= self.distance.values[0] < 300:
            self.tarrifs = 2.15
        elif 300 <= self.distance.values[0] < 500:
            self.tarrifs = 1.85
        else:
            self.tarrifs = 1.58
        

    def calculator (self):
        
        self.check_weight()
        self.distance_between_city()
        self.distance_tarrifs ()
        transportation_cost = int(self.distance.values[0]) * self.weight *self.tarrifs
        result = f'Вартість перевезення за напрямком {self.point1}-{self.point2} становить {round(transportation_cost,2)} грн.'
               
        
        label_result = tk.Label(self.backgr, text=result,bg= '#8cc983', fg = '#000000')
        label_result.place(x=5, y=400)

    def elevator_calculate(self,price,number_of_days):
        
        self.check_weight()
        self.grain_type_index()
        conditional_weight = self.weight/self.index_dict.get(self.combobox_type.get())
        elevator_result = float(price)*float(number_of_days)*conditional_weight 
        text_elevator_result=f'Вартість послуг зберігання зернової культури становить {round(elevator_result,2)} грн.'
        label_elevator_result = tk.Label(self.backgr, text = text_elevator_result,bg = '#8cc983', fg = '#000000')
        label_elevator_result.place(x=5, y=420)



class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        

    def init_child(self):
        self.title('Вартість послуг елеватора')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_entry_city1 = tk.Label(self, text='Ціна зберігання за 1 тонно-добу')
        label_entry_city1.place(x=30, y=50)
        
        label_entry_city2 = tk.Label(self, text='Кількість діб')
        label_entry_city2.place(x=30, y=100)

        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=220, y=50)

        self.entry_number_of_days = ttk.Entry(self)
        self.entry_number_of_days.place(x=220, y=100)

        btn_cancel = ttk.Button(self, text='Закрити', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Ввести' )
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>',lambda event : self.view.elevator_calculate(self.entry_price.get(),self.entry_number_of_days.get()))

        self.grab_set()
        
     
    def elevator_cost(self,price,number_of_days):
        
        price = float(self.entry_price.get())
        number_of_days = float(self.entry_number_of_days.get())
       


if __name__ == "__main__":
    root = tk.Tk()   
    root.title("Агрологістичний калькулятор")
    root.geometry("420x550")
    root.resizable(False, False)
    app = Main(root)
    root.mainloop()
