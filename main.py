from tkinter import *
from tkinter import messagebox, Listbox, simpledialog
import tkinter as tk
import re
import os
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk

class TextFormating:
    def search_re(pattern, text, groupid=0):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append(
                    (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
                )
        return matches

    def rgb(rgb):
        return "#%02x%02x%02x" % rgb
    
class Contstants:


    root = Tk()

    hubName = "HUB_FLL08"
    pybrikcsDirectory = "/Library/Frameworks/Python.framework/Versions/3.12/bin/pybricksdev"
    fileName = "main.py"
    specific_file_names = ["demo.py", "demoRide.py", "testRide.py"]
    githubString = "Off"
    directory_path = "/Users/antoninsiska/Documents/fll"

    rides = {
        "Red": "None",
        "Green": "None",
        "Black": "None",
        "Pink": "None",
        "Purple": "None",
        "Yellow": "None",
        "Blue": "None"

    }

    # Načtení obrázku
    image_path = '/Users/antoninsiska/Documents/Gravel-app/image.jpeg'

    previousText = ''

    normal = TextFormating.rgb((234, 234, 234))
    keywords = TextFormating.rgb((234, 95, 95))
    comments = TextFormating.rgb((95, 234, 165))
    string = TextFormating.rgb((234, 162, 95))
    function = TextFormating.rgb((95, 211, 234))
    background = TextFormating.rgb((42, 42, 42))
    commands = TextFormating.rgb((40, 135, 255))
    nums = TextFormating.rgb((102, 133, 218))
    lastColour = TextFormating.rgb((255, 135, 135))
    font = 'Consolas 15'

    # Define a list of Regex Patterns that should be colored in a certain way
    repl = [
        ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
        ['".*?"', string],
        ['\'.*?\'', string],
        ['#.*?$', comments],
        ['Straight|Turn|Curve|TurnTool|GoTo|GetXY|InitialValue|SmoothTurn|Tool', commands],
        ["1|2|3|4|5|6|7|8|9|0|True|False", nums],
        ["last", lastColour]
    ]

    # Make the Text Widget
    editArea = Text(
        root,
        background=background,
        foreground=normal,
        insertbackground=normal,
        relief=FLAT,
        borderwidth=30,
        font=font
    )
    editArea.pack(fill=BOTH, expand=1)

    # Vytvoření listboxu pro soubory
    

    # Přesunutí editArea na správné místo pomocí grid
    editArea.pack(side=RIGHT, fill=BOTH, expand=1)

    # Nastavení mřížky na pružné roztažení
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

class Map:
    def __init__(self):
        pass

    def handle_image_click(event):
        global background_color
        x, y = event.x, event.y
        clicked_color = img.getpixel((x, y))
        
        if clicked_color == background_color:
            return  # Ignoruje kliknutí na pozadí

        # Určení akce na základě barvy čáry
        if clicked_color[0] >= 230 and clicked_color[1] <= 50 and clicked_color[2] <= 70:  # Červená
            messagebox.showinfo("Akce", "Otevření souboru pro červenou čáru")
            Files.open_specific_file("demo.py")

        elif clicked_color[0] <= 100 and clicked_color[1] >= 200 and clicked_color[2] >= 50:  # Zelená
            messagebox.showinfo("Akce", "Otevření souboru pro zelenou čáru")
            Files.open_specific_file("demoRide.py")

        elif clicked_color[0] <= 30 and clicked_color[1] <= 120 and clicked_color[2] >= 240:  # Modrá
            messagebox.showinfo("Akce", "Otevření souboru pro modrou čáru")
            Files.open_specific_file("testRide.py")
        
        elif clicked_color[0] <= 5 and clicked_color[1] <= 5 and clicked_color[2] <= 5:
            messagebox.showinfo("Akce", "Kliknuto na černou")

        elif clicked_color[0] >= 210 and clicked_color[1] >= 195 and clicked_color[2] <= 50:
            messagebox.showinfo("Akce", "Kliknuto na žlutou barvu")

        elif clicked_color[0] <= 155 and clicked_color[1] <= 60 and clicked_color[2] >= 160:
            messagebox.showinfo("Akce", "Kliknuto na fialovou")
        else:
            messagebox.showinfo("Info", f"Kliknutí na neznámou barvu: {clicked_color}")


    def Open():
        global image_path, img_tk, img
        # Druhé okno pro zobrazení obrázku
        image_window = Toplevel(root)
        image_window.geometry('1000x600')
        image_window.title("Obrázek s čárami")

        # Zobrazení obrázku v druhém okně
        canvas = Canvas(image_window, width=img.width, height=img.height)
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=img_tk)
        canvas.bind("<Button-1>", Map.handle_image_click)

        return image_window

class Files:
    

    def Open():
        global image_path, img_tk, img
        # Druhé okno pro zobrazení obrázku
        image_window = Toplevel(root)
        image_window.geometry('1000x600')
        image_window.title("Obrázek s čárami")

        # Zobrazení obrázku v druhém okně
        canvas = Canvas(image_window, width=img.width, height=img.height)
        canvas.pack()
        canvas.create_image(0, 0, anchor=NW, image=img_tk)
        canvas.bind("<Button-1>", Map.handle_image_click)

        return image_window

    def open_specific_file(filename):
        editArea = Contstants.editArea
        if filename == "None" or filename == None:
            messagebox.showerror("No file", "You havent set any file")
        else:
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    editArea.delete('1.0', END)
                    editArea.insert('1.0', content)
            except Exception as e:
                messagebox.showerror("Chyba", f"Soubor nelze otevřít: {e}")


    def load_selected_file(event=None):
        global current_file
        editArea = Contstants.editArea
        if file_list.curselection():
            selected_file = file_list.get(file_list.curselection())
            file_path = os.path.join(Contstants.directory_path, selected_file)
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    editArea.delete('1.0', END)
                    editArea.insert('1.0', content)
                    current_file = file_path
                    global previousText
                    previousText = content
                    Files.changes()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file: {e}")
        else:
            messagebox.showwarning("Warning", "No file selected.")

    def load_files(directory):
        file_list.delete(0, tk.END)
        try:
            for file_name in os.listdir(directory):
                if file_name.endswith(".py") and file_name in Contstants.specific_file_names:
                    file_list.insert(tk.END, file_name)
        except FileNotFoundError:
            messagebox.showerror("Error", "Directory not found!")


    def SaveFile(event=None):
        global current_file
        editArea = Contstants.editArea
        if current_file:
            with open(current_file, 'w', encoding='utf-8') as f:
                f.write(editArea.get('1.0', END))
            
            Others.VerifyCommand(['sh', '-c', f'cd {Contstants.directory_path} && {Contstants.pybrikcsDirectory} run ble -n {Contstants.hubName} {Contstants.fileName}'])
        else:
            messagebox.showwarning("Warning", "No file opened.")
        
        messagebox.showinfo("Info", "Soubor se uložil")



    def changes(event=None):
        global previousText
        editArea = Contstants.editArea
        if editArea.get('1.0', END) == previousText:
            return

        for tag in editArea.tag_names():
            editArea.tag_remove(tag, "1.0", "end")

        i = 0
        for pattern, color in Contstants.repl:
            for start, end in TextFormating.search_re(pattern, editArea.get('1.0', END)):
                editArea.tag_add(f'{i}', start, end)
                editArea.tag_config(f'{i}', foreground=color)
                i += 1

        previousText = editArea.get('1.0', END) 

class Rides:

    def Red():
        Files.open_specific_file(Contstants.rides["Red"])
    def Green():
        Files.open_specific_file(Contstants.rides["Green"])
    def Black():
        Files.open_specific_file(Contstants.rides["Black"])
    def Pink():
        Files.open_specific_file(Contstants.rides["Pink"])
    def Purple():
        Files.open_specific_file(Contstants.rides["Purple"])
    def Yellow():
        Files.open_specific_file(Contstants.rides["Yellow"])
    def Blue():
        Files.open_specific_file(Contstants.rides["Blue"])

class Settings:

    def open_settings():
        global directory_path, specific_file_names, fileName

        # Možnost výběru složky
        new_directory_path = filedialog.askdirectory(title="Select Directory Path", initialdir=Contstants.directory_path)
        if new_directory_path:
            Contstants.directory_path = new_directory_path

        # Možnost výběru specifických souborů
        selected_files = filedialog.askopenfilenames(
            title="Select Specific Files",
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*")),
            initialdir=Contstants.directory_path
        )
        if selected_files:
            Contstants.specific_file_names = [os.path.basename(file) for file in selected_files]

        

        Files.load_files(Contstants.directory_path)

    def HubNameSettings():
        global hubName
        newHubName = simpledialog.askstring("Hub name", "Enter new hub name:", initialvalue=Contstants.hubName)
        if newHubName:
            Contstants.hubName = newHubName

    def PybricksDirectorySettigns():
        global pybricksDirectory
        newPybricksDirectory = simpledialog.askstring("Pybricks directory", "Enter pybricks directory:", initialvalue=Contstants.pybrikcsDirectory)
        if newPybricksDirectory:
            Contstants.pybrikcsDirectory = newPybricksDirectory

    def DemoFileSettings():
        global demoFileName
        # Možnost výběru demo souboru
        demo_file_path = filedialog.askopenfilename(
            title="Select Demo File",
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*")),
            initialdir=Contstants.directory_path
        )
        if demo_file_path:
            Contstants.fileName = os.path.basename(demo_file_path)

    def ImageDirectorySettings():
        
        newImageDirectory = simpledialog.askstring("Image directory", "Enter image directory:", initialvalue="")
        if newImageDirectory:
            Contstants.imageDirectory = newImageDirectory

    def SetGithub(ask = True):
        githubPass = simpledialog.askstring("Image directory", "Enter image directory:", initialvalue=Contstants.githubString)

        if githubPass == "TondaFLL":
            return True
        else:
            return False

class GitHub:

    def GetCommit():
        githubBool = Settings.SetGithub(ask=False)
        if githubBool:
            commit = simpledialog.askstring("Commit message", "Enter commit message:")
            Others.VerifyCommand(["git", "add", "."], cwd=Contstants.directory_path)
            Others.VerifyCommand(['git', 'commit', '-m', commit], cwd=Contstants.directory_path)
            Others.VerifyCommand(['git', 'push'], cwd=Contstants.directory_path)
        else:
            messagebox.showwarning("GitHub control", "Bad password")
        

    def Pull():
        githubBool = Settings.SetGithub(ask=False)
        if githubBool:
            Others.VerifyCommand(['git', 'pull'])
        else:
            messagebox.showwarning("GitHub control", "Bad password")
    
class Others:

    

    def execute(event=None):
        global current_file

        pybrikcsDirectory = Contstants.pybrikcsDirectory
        fileName = Contstants.fileName

        messagebox.showinfo("Info", "Program se po kliknutí na OK nahraje a spustí.")

        if current_file:
            with open(current_file, 'w', encoding='utf-8') as f:
                f.write(editArea.get('1.0', END))
            
            Others.VerifyCommand(['sh', '-c', f'cd {Contstants.directory_path} && {Contstants.pybrikcsDirectory} run ble -n {Contstants.hubName} {Contstants.fileName}'])
        else:
            messagebox.showwarning("Warning", "No file opened.")


    def VerifyCommand(command:list, cwd=None):
        try:
            result = subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                        cwd=cwd
                    )
            if result.returncode == 0:
                messagebox.showinfo("Success", "Command executed successfully!")
            else:
                messagebox.showerror("Error", f"Command failed: {result.stderr}")
        except Exception as e:
                messagebox.showerror("Error", f"Execution failed: {e}")

        print(result.returncode)
        print(result.stdout)
        print(result.stderr)

class MenuBar:

    root = Contstants.root

    # Setup Menu Bar
    menu_bar = Menu(root)
    settings_menu = Menu(menu_bar, tearoff=0)
    settings_menu.add_command(label="Edit Directory Path", command=Settings.open_settings)
    settings_menu.add_command(label="Edit Specific File Names", command=Settings.open_settings)
    settings_menu.add_command(label="Pybricks directory", command=Settings.PybricksDirectorySettigns)
    settings_menu.add_command(label="Image directory", command=Settings.ImageDirectorySettings)
    settings_menu.add_command(label="Hub name", command=Settings.HubNameSettings)
    settings_menu.add_command(label="Demo file", command=Settings.DemoFileSettings)
    settings_menu.add_command(label="Github", command=Settings.SetGithub)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    root.config(menu=menu_bar)

    controls_menu = Menu(menu_bar, tearoff=1)
    menu_bar.add_cascade(label="Control", menu=controls_menu)
    controls_menu.add_command(label="Upload and run", command=Others.execute)
    controls_menu.add_command(label="Create commit", command=GitHub.GetCommit)
    controls_menu.add_command(label="Pull", command=GitHub.Pull)
    controls_menu.add_command(label="Save", command=Files.SaveFile)
    controls_menu.add_command(label="Open map", command=Map.Open)
    


    rides_menu = Menu(menu_bar, tearoff=2)
    menu_bar.add_cascade(label="Rides", menu=rides_menu)
    rides_menu.add_command(label="Red", command=Rides.Red)
    rides_menu.add_command(label="Green", command=Rides.Green)
    rides_menu.add_command(label="Black", command=Rides.Black)
    rides_menu.add_command(label="Blue", command=Rides.Blue)
    rides_menu.add_command(label="Yellow", command=Rides.Yellow)
    rides_menu.add_command(label="Purlple", command=Rides.Purple)
    rides_menu.add_command(label="Pink", command=Rides.Pink)

class ButtonActions:

    # Define button actions
    def button1_action():
        messagebox.showinfo("Button 1", "Button 1 was clicked!")

    def button2_action():
        messagebox.showinfo("Button 2", "Button 2 was clicked!")

    def button3_action():
        messagebox.showinfo("Button 3", "Button 3 was clicked!")

    def button4_action():
        messagebox.showinfo("Button 4", "Button 4 was clicked!")

# Nastavení Tkinter
root = Contstants.root
root.geometry('1000x1000')
root.title("Gravel")

image_path = Contstants.image_path

img = Image.open(image_path)
img = img.resize((1000, 600))
img_tk = ImageTk.PhotoImage(img)

# Otevření okna s obrázkem
background_color = img.getpixel((0, 0))

file_list_frame = tk.Frame(root, bg="#2d2d2d", width=100)
file_list_frame.pack(side=tk.LEFT, fill=tk.Y)

# Listbox for files
file_list = tk.Listbox(file_list_frame, bg="#333333", fg="white", selectbackground="#444444")
file_list.pack(fill=tk.BOTH, expand=True)

# Variable to track the currently opened file
current_file = None
editArea = Contstants.editArea
# Add buttons below the file_list
button1 = tk.Button(file_list_frame, text="Commit message", command=GitHub.GetCommit)
button2 = tk.Button(file_list_frame, text="Pull", command=GitHub.Pull)
button3 = tk.Button(file_list_frame, text="Get info")
button4 = tk.Button(file_list_frame, text="Button 4", command=ButtonActions.button4_action)

button1.pack(fill=tk.X, padx=5, pady=2)
button2.pack(fill=tk.X, padx=5, pady=2)
button3.pack(fill=tk.X, padx=5, pady=2)
button4.pack(fill=tk.X, padx=5, pady=2)

Files.load_files(Contstants.directory_path)

file_list.bind('<ButtonRelease-1>', Files.load_selected_file)
editArea.bind('<KeyRelease>', Files.changes)
root.bind('<Command-r>', Others.execute)
root.bind('<Command-s>', Files.SaveFile)

root.mainloop()