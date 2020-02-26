"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 1.0
Details : 
    - 2020/01/09 Software creation 
    - 2020/02/14 Executable version 0.4
    - 2020/02/24 Implementation of I/V version 1.0

File description : Application Launcher

"""

from View import View

if __name__ == "__main__":
    app = View()
    app.title("CBRAM cells programmer")
    app.mainloop()