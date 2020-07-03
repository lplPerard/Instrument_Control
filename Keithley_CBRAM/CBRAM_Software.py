"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 3.0
Details : 
    - 2020/01/09 Software creation 
    - 2020/02/14 Executable version 0.4
    - 2020/02/24 Implementation of I/V version 1.0
    - 2020/05/05 Implementation of Modelling version 2.0
    - 2020/05/06 Implementation of temperature in Modelling version 2.1
    - 2020/06/26 Bug corrections and implementation of signal choice for Cycling and auto mailing
    - 2020/07/02 Implementation of Stability version 3.0

File description : Application Launcher

"""

from View import View

if __name__ == "__main__":
    app = View()
    app.title("CBRAM cells programmer")
    app.mainloop()