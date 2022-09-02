from tkinterdnd2 import TkinterDnD

from gui.gui import InitialScreen

root = TkinterDnD.Tk()
root.geometry('1500x900')

InitialScreen(root)

root.mainloop()
