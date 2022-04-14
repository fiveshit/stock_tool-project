import tkinter as tk
from View.View import Stock_View
from Model import Stock_Mode
from Controller import Stock_Controller
class Stock_APP(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('stock app')
        self.geometry('820x650')


        
        # create a View 
        view = Stock_View(self)

        # creat a Model 
        model = Stock_Mode()

        # create a cotroller
        controller = Stock_Controller(view,model)

        # set view to controller
        
        
if __name__ == '__main__':
    app = Stock_APP()
    app.mainloop()
