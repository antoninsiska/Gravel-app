import tkinter as tk
from tkinter import Menu

# Inicializace hlavního okna
root = tk.Tk()
root.title("Menu s vnořeným submenu")

# Vytvoření hlavního menu
menu_bar = Menu(root)

# Vytvoření hlavního submenu
submenu = Menu(menu_bar, tearoff=0)

# Vytvoření submenu pro "Možnost 1"
submenu_option1 = Menu(submenu, tearoff=1)
submenu_option1.add_command(label="Podmožnost 1.1", command=lambda: print("Zvoleno: Podmožnost 1.1"))
submenu_option1.add_command(label="Podmožnost 1.2", command=lambda: print("Zvoleno: Podmožnost 1.2"))

# Přidání "Možnost 1" s dalším submenu
submenu.add_cascade(label="Možnost 1", menu=submenu_option1)
submenu.add_command(label="Možnost 2", command=lambda: print("Zvoleno: Možnost 2"))

# Přidání hlavní položky s podmenu
menu_bar.add_cascade(label="Hlavní položka", menu=submenu)

# Přidání menu do hlavního okna
root.config(menu=menu_bar)

# Spuštění aplikace
root.mainloop()
