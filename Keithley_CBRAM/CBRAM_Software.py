"""Copyright Grenoble-inp LCIS

Developped by : Luc PERARD
Version : 0.0
Details : 
    - 2020/01/09 Software creation 

File description : Application Launcher

"""

from View import View

if __name__ == "__main__":
    app = View()
    app.title("CBRAM cells programmer")
    app.mainloop()