
from Controller.Controller import Stock_Controller
#---------------------------------------#
#Name : Main functions
#Description : run from controller
#---------------------------------------#
class Stock_APP():
    def __init__(self):

        self.controller = Stock_Controller() 
        
if __name__ == '__main__':
    app = Stock_APP()
    app.controller.run()
