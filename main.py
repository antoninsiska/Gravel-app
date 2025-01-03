from tkinter import *
from tkinter import messagebox, Listbox, simpledialog, font, filedialog
import tkinter as tk
from tkinter.ttk import Progressbar
from collections import deque
import re
import os
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk
from markdown2 import Markdown
from tkhtmlview import HTMLLabel
from tkinter import messagebox as mbox
from tklinenums import TkLineNumbers
import json
from tkinter.scrolledtext import ScrolledText
import threading
import asyncio


first = True

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
    
    def InstertTab(event=False):
        cursor_position = Contstants.editArea.index("insert")  # Zjistí pozici kurzoru
        Contstants.editArea.insert(cursor_position, "    ")  # Vloží text na tuto pozici
        return "break"
    
    def DeleteLine(event):
        # Zjistí aktuální pozici kurzoru
        cursor_position = Contstants.editArea.index("insert")
        # Zjistí začátek aktuálního řádku
        line_start = Contstants.editArea.index(f"{cursor_position.split('.')[0]}.0")
        # Smaže od začátku řádku až po kurzor
        Contstants.editArea.delete(line_start, cursor_position)
        return "break"  # Zabrání standardní akci klávesy

    def Undo(event=False):
        try:
            Contstants.editArea.edit_undo()  # Provede zpětnou akci
        except tk.TclError:
            pass
class Contstants:


    root = Tk()

    gitHubCommit = False

    
    

    hubName = "HUB_FLL08"
    pybrikcsDirectory = "/Library/Frameworks/Python.framework/Versions/3.12/bin/pybricksdev"
    fileName = "demo.py"
    specific_file_names = ["demo.py"]
    githubString = "Off"
    directory_path = "/Users/antoninsiska/Documents/fll/"
    

    rides = {
        "Red": "demo.py",
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
        ['Straight|Turn|Curve|TurnTool|GoTo|GetXY|InitialValue|SmoothTurn|Tool', commands],
        ["1|2|3|4|5|6|7|8|9|0|True|False", nums],
        ["last", lastColour],
        ['".*?"', string],
        ['\'.*?\'', string],
        ['"""', string],
        ['#.*?$', comments],
    ]

    # Make the Text Widget
    editArea = Text(
        root,
        background=background,
        foreground=normal,
        insertbackground=normal,
        relief=FLAT,
        borderwidth=30,
        font=font,
        undo=True
    )
    editArea.pack(fill=BOTH, expand=1)

    # Vytvoření listboxu pro soubory
    

    # Přesunutí editArea na správné místo pomocí grid
    editArea.pack(side=RIGHT, fill=BOTH, expand=1)

    # Nastavení mřížky na pružné roztažení
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)


    
    

    file_list_frame = tk.Frame(root, bg="#2d2d2d")
    file_list_frame.pack(side=tk.LEFT, fill=tk.Y, expand=1)

    jsonFileName = "data.json"

    line_count = 0
    
    yes = True

    saved = False
    
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
            file_path = os.path.join(Contstants.directory_path, filename)
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    editArea.delete('1.0', END)
                    editArea.insert('1.0', content)
                    editArea.edit_reset()
                    
            except Exception as e:
                messagebox.showerror("Chyba", f"Soubor nelze otevřít: {e}")


    def load_selected_file(event=None):
        global current_file
        editArea = Contstants.editArea
        if file_list.curselection():
            selected_file = file_list.get(file_list.curselection())
            file_path = os.path.join(Contstants.directory_path, selected_file)
            #try:
            with open(file_path, "r") as file:
                content = file.read()
                editArea.delete('1.0', END)
                editArea.insert('1.0', content)
                current_file = file_path
                global previousText
                previousText = content
                Files.changes()
                root.after_idle(linenums.redraw)
                Contstants.saved = True
                editArea.edit_reset()
                
            #except Exception as e:
                #messagebox.showerror("Error", f"Could not load file: {e}")
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
            Contstants.saved = True
            MenuBar.Update()
            
        else:
            messagebox.showwarning("Warning", "No file opened.")
        
        messagebox.showinfo("Info", "Soubor se uložil")


    last_line = 0
    previousText = Contstants.editArea.get('1.0', END) 
    def changes(event=None):
        global previousText
        global last_line
        
        Contstants.saved = False

        MenuBar.Update()

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
        MenuBar.Update()

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

    def JsonFileDirecotry(event=False):
        
        # Možnost výběru demo souboru
        json_file_path = filedialog.askopenfilename(
        title="Select Demo File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")),
        initialdir=Contstants.jsonFileName
    )
        print(json_file_path)
        if json_file_path:
            Contstants.jsonFileName = str(json_file_path)
            print("Vybraný soubor:", Contstants.jsonFileName)
        


    def SetDeafult1():
        Contstants.hubName = "HUB_FLL08"
        MenuBar.Update()

    def SetDeafult2():
        Contstants.hubName = "HUB_FLL07"
        MenuBar.Update()

class GitHub:

   

    def GetCommit():
        githubBool = True
        if githubBool:
            a = messagebox.askquestion("GitHub", "Opravdu cheš vytvořit commit")
            if a == "yes":
                commit = simpledialog.askstring("Commit message", "Enter commit message:")
                Others.VerifyCommand(["git", "add", "."], cwd=Contstants.directory_path)
                Others.VerifyCommand(['git', 'commit', '-m', commit], cwd=Contstants.directory_path)   
                Contstants.gitHubCommit = True
                MenuBar.Update()
     
        

    def Pull():
        a = messagebox.askquestion("GitHub", "Opravdu chceš vytvořit pull")
        if a == "yes":
            githubBool = Settings.SetGithub(ask=False)
            if githubBool:
                Others.VerifyCommand(['git', 'pull'])
        

    def Push():
        a = messagebox.askquestion("GitHub", "Opravdu chceš nahrát commit na github.")
        if a == "yes":
            Others.VerifyCommand(['git', 'push'], cwd=Contstants.directory_path)
            Contstants.gitHubCommit = False
            MenuBar.Update()

class CMDViewer:
    def __init__(self, root, command):
        self.root = root
        self.loop = asyncio.new_event_loop()
        self.command = command

        # Uchování posledních tří řádků výstupu
        self.last_lines = deque(maxlen=3)

        # Spustí asyncio smyčku v samostatném vlákně
        self.thread = threading.Thread(target=self.start_asyncio_loop, args=(self.loop,), daemon=True)
        self.thread.start()

        # Automatické spuštění příkazu
        self.open_new_window(self.command)

    def open_new_window(self, command):
        # Vytvoření nového okna
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title(f"Command: {command}")

        self.output_widget = ScrolledText(self.new_window, height=20, width=80)
        self.output_widget.pack(padx=10, pady=10)

        # Spuštění příkazu asynchronně
        self.start_command(command, self.output_widget)

    def start_command(self, command, output_widget):
        asyncio.run_coroutine_threadsafe(self.run_command(command, output_widget), self.loop)

    async def run_command(self, command, output_widget):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        async def read_stream(stream, tag):
            while True:
                data = await stream.read(256)
                if not data:
                    break
                text = data.decode()

                # Ukládání posledních tří řádků do textového okna
                self.root.after(0, self.append_output, output_widget, text)

        # Spuštění čtení stdout a stderr současně
        await asyncio.gather(
            read_stream(process.stdout, "stdout"),
            read_stream(process.stderr, "stderr")
        )

        await process.wait()

        # Zavření okna a zobrazení analýzy posledních řádků
        self.root.after(1000, self.analyze_and_show_last_lines)

    def append_output(self, output_widget, text):
        output_widget.insert(tk.END, text)
        output_widget.see(tk.END)
        # Uchováme poslední řádky pro analýzu
        self.last_lines.append(text.strip())

    def analyze_and_show_last_lines(self):
        # Analýza posledních tří řádků
        last_output = "\n".join(self.last_lines)

        # Pokud se objeví traceback (chyba), zobrazíme poslední tři řádky
        if any("Traceback (most recent call last)" in line for line in self.last_lines):
            messagebox.showerror("Error Detected", f"Error occurred:\n\n{last_output}")
        elif "SystemExit" in last_output:
            # Pokud je SystemExit, zobrazíme pouze poslední řádek
            messagebox.showinfo("Program Stopped", f"Program finished with SystemExit:\n\n{self.last_lines[-1]}")
        elif self.last_lines:
            # Pokud není chyba, zobrazíme poslední řádek
            messagebox.showinfo("Program Stopped", f"Program finished:\n\n{self.last_lines[-1]}")

        # Zavření okna po zobrazení hlášení
        self.new_window.after(1000, self.new_window.destroy)

    def start_asyncio_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

class Others:

    

    def execute(event=None):
        global current_file

        pybrikcsDirectory = Contstants.pybrikcsDirectory
        fileName = Contstants.fileName

         

        messagebox.showinfo("Info", "Program se po kliknutí na OK nahraje a spustí.")
        upload = messagebox.askquestion("Info", "Opravdu chceš nahrát program do robota")
        if current_file and upload == "yes":
            with open(current_file, 'w', encoding='utf-8') as f:
                f.write(editArea.get('1.0', END))
            print("{", Contstants.directory_path)
            print("{", Contstants.hubName)
            print("{", Contstants.fileName)
            CMDViewer(Contstants.root, command=f"cd {Contstants.directory_path} && {Contstants.pybrikcsDirectory} run ble -n {Contstants.hubName} {Contstants.fileName}")

            """Others.VerifyCommand(['sh', '-c', f'cd {Contstants.directory_path} && {Contstants.pybrikcsDirectory} run ble -n {Contstants.hubName} {Contstants.fileName}'])
        else:
            messagebox.showwarning("Warning", "No file opened.")"""


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


class Json:
    
    def Load():
        try:
            with open(Contstants.jsonFileName, "r") as file:
                data = json.load(file)
        except:
            messagebox.showerror("JSON file", f"Bad Json file directory: {Contstants.jsonFileName}")
            Settings.JsonFileDirecotry()
            Json.LoadAndTestData()

        Contstants.hubName = data['data'][0]['hubName']
        Contstants.pybrikcsDirectory = data['data'][0]['pybrikcsDirectory']
        Contstants.fileName = data['data'][0]['fileName']
        Contstants.directory_path = data['data'][0]['directoryPath']
        Contstants.rides = data['data'][0]['rides'][0]
        Contstants.specific_file_names = data['data'][0]['specificFileNames']
        Contstants.image_path = data['data'][0]['imagePath']
        
        
    
    def LoadAndTestData(event = False):
        print("_________________")
        print(Contstants.hubName)
        print(Contstants.pybrikcsDirectory)
        print(Contstants.fileName)
        print(Contstants.directory_path)
        print(Contstants.image_path)
        print(Contstants.rides)
        print(Contstants.specific_file_names)
        print("------------------------")
        Json.Load()
        MenuBar.Update()
        Files.load_files(Contstants.directory_path)
        print(Contstants.hubName)
        print(Contstants.pybrikcsDirectory)
        print(Contstants.fileName)
        print(Contstants.directory_path)
        print(Contstants.image_path)
        print(Contstants.rides)
        print(Contstants.specific_file_names)
        print("------------------------")
        


        

class MenuBar:
    
    root = Contstants.root 
    

    # Setup Menu Bar
    menu_bar = Menu(root)
    settings_menu = Menu(menu_bar, tearoff=0)

     # Nastavení submenu pro Hub name
    hub_name_submenu = Menu(settings_menu, tearoff=5)
    hub_name_submenu.add_command(label="HUB_FLL_08", command=Settings.SetDeafult1)
    hub_name_submenu.add_command(label="HUB_FLL_07", command=Settings.SetDeafult2)
        

    settings_menu.add_command(label="Edit Directory Path", command=Settings.open_settings)
    settings_menu.add_command(label="Edit Specific File Names", command=Settings.open_settings)
    settings_menu.add_command(label="Pybricks directory", command=Settings.PybricksDirectorySettigns)
    settings_menu.add_command(label="Image directory", command=Settings.ImageDirectorySettings)
    settings_menu.add_cascade(label="Set json file directory", command=Settings.JsonFileDirecotry)
    settings_menu.add_cascade(label="Hub name", menu=hub_name_submenu)

    settings_menu.add_command(label="Demo file", command=Settings.DemoFileSettings)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    root.config(menu=menu_bar)

    controls_menu = Menu(menu_bar, tearoff=1)
    menu_bar.add_cascade(label="Control", menu=controls_menu)
    controls_menu.add_command(label="Upload and run", command=Others.execute)
    controls_menu.add_command(label="Create commit", command=GitHub.GetCommit)
    controls_menu.add_command(label="Push", command=GitHub.Push)
    controls_menu.add_command(label="Pull", command=GitHub.Pull)
    controls_menu.add_command(label="Save", command=Files.SaveFile)
    controls_menu.add_command(label="Reload json", command=Json.LoadAndTestData)
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

    file_list_frame = Contstants.file_list_frame

    text1 = Label(file_list_frame, text=Contstants.hubName)
    text2 = Label(file_list_frame, text="nothing commited")
    text3 = Label(file_list_frame, text="[     ]")

    def Update():
        MenuBar.text1.config(text=Contstants.hubName)

        if Contstants.gitHubCommit:
            text = "COMMITED"
        else:
            text = "nothing commited"

        MenuBar.text2.config(text=text)
        print(Contstants.saved)
        if Contstants.saved == True:
            MenuBar.text3.config(text="[     ]")
        else:
            MenuBar.text3.config(text="[██]")
        

class ButtonActions:
    def __init__(self):
        self.rides = Contstants.rides
    # Define button actions
    def button1_action():
        messagebox.showinfo("Button 1", "Button 1 was clicked!")

    def button2_action():
        messagebox.showinfo("Button 2", "Button 2 was clicked!")

    def button3_action():
        messagebox.showinfo("Button 3", "Button 3 was clicked!")

    def button4_action():
        messagebox.showinfo("Button 4", "Button 4 was clicked!")
    
    def OpenRed(event=False):
        Files.open_specific_file(filename=Contstants.rides["Red"])
        Files.changes()

    def OpenGreen(event=False):
        Files.open_specific_file(filename=Contstants.rides["Green"])
        Files.changes()

    def OpenBlue(event=False):
        Files.open_specific_file(filename=Contstants.rides["Blue"])
        Files.changes()

class Window:
    def __init__(self, master=None):
        self.rootMD = Toplevel(master)
        self.myfont = font.Font(family="Helvetica", size=14)
        self.init_window()
        self.openfile()

    def init_window(self):
        self.rootMD.title("TDOWN")

        self.rootMD.geometry("850x500")
        # Vytvoření input editoru
        self.inputeditor = Text(self.rootMD, width=1, font=self.myfont)
        self.inputeditor.pack(fill=BOTH, expand=1, side=LEFT)

        # Vytvoření výstupního boxu
        self.outputbox = HTMLLabel(self.rootMD, width=1, background="white")
        self.outputbox.pack(fill=BOTH, expand=1, side=RIGHT)
        self.outputbox.fit_height()

        # Bind event pro změnu inputu
        self.inputeditor.bind("<<Modified>>", self.onInputChange)

        # Vytvoření hlavního menu
        self.mainmenu = Menu(self.rootMD)
        self.filemenu = Menu(self.mainmenu)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_command(label="Save as", command=self.savefile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.rootMD.quit)
        self.mainmenu.add_cascade(label="File", menu=self.filemenu)
        self.rootMD.config(menu=self.mainmenu)

    def onInputChange(self, event):
        self.inputeditor.edit_modified(0)
        md2html = Markdown()
        markdownText = self.inputeditor.get("1.0", END)
        html = md2html.convert(markdownText)
        self.outputbox.set_html(html)

    def openfile(self):
        openfilename = Contstants.directory_path + "/README.MD" 

        """filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),("Text File", "*.txt"), ("All Files", "*.*")))"""
        if openfilename:
            try:
                self.inputeditor.delete(1.0, END)
                self.inputeditor.insert(END, open(openfilename).read())
            except:
                mbox.showerror("Error Opening Selected File", "Oops!, The file you selected: {} cannot be opened!".format(openfilename))
    
    def savefile(self):
        filedata = self.inputeditor.get("1.0", END)
        savefilename = filedialog.asksaveasfilename(filetypes=(("Markdown File", "*.md"),
                                                                ("Text File", "*.txt")), title="Save Markdown File")
        if savefilename:
            try:
                with open(savefilename, "w") as f:
                    f.write(filedata)
            except:
                mbox.showerror("Error Saving File", "Oops!, The File: {} cannot be saved!".format(savefilename))

class ToolBox:

    def OpenWindow(event=False):
        root = Toplevel(Contstants.root)
        root.geometry("200x50")
        btn1 = tk.Button(root, text="Green", command=ButtonActions.OpenGreen)
        btn1.pack(padx=5, pady=5)


    

# Nastavení Tkinter
root = Contstants.root
root.geometry('1100x1000')
root.title("Gravel")

image_path = Contstants.image_path

img = Image.open(image_path)
img = img.resize((1000, 600))
img_tk = ImageTk.PhotoImage(img)

# 
# Otevření okna s obrázkem
background_color = img.getpixel((0, 0))

file_list_frame = Contstants.file_list_frame

# Listbox for files
file_list = tk.Listbox(file_list_frame, bg="#333333", fg="white", selectbackground="#444444")
file_list.pack(fill=tk.BOTH, expand=1)

# Variable to track the currently opened file
current_file = None
editArea = Contstants.editArea
print("yview", editArea.yview())

# Add buttons below the file_list
button1 = tk.Button(file_list_frame, text="Commit message", command=GitHub.GetCommit)
button2 = tk.Button(file_list_frame, text="Toolbox", command=ToolBox.OpenWindow)
button3 = tk.Button(file_list_frame, text="Push", command=GitHub.Push)
button4 = tk.Button(file_list_frame, text="Markdown editor", command=Window)
button5 = tk.Button(file_list_frame, text="")


MenuBar.text1.pack(fill=tk.X, padx=5, pady=2)
MenuBar.text2.pack(fill=tk.X, padx=5, pady=2)
MenuBar.text3.pack(fill=tk.X, padx=5, pady=2)
button1.pack(fill=tk.X, padx=5, pady=2)
button2.pack(fill=tk.X, padx=5, pady=2)
button3.pack(fill=tk.X, padx=5, pady=2)
button4.pack(fill=tk.X, padx=5, pady=2)

linenums = TkLineNumbers(root, editArea, justify="center", colors=("#FFFFFF", "#292929"))
linenums.pack(fill="y", side="left")

# Redraw the line numbers when the text widget contents are modified
editArea.bind("<<Modified>>", lambda event: root.after_idle(linenums.redraw), add=True)
editArea.bind("<Return>", lambda event: root.after_idle(linenums.redraw), add=True)
editArea.bind("<BackSpace>", lambda event: root.after_idle(linenums.redraw), add=True)


Files.load_files(Contstants.directory_path)

file_list.bind('<ButtonRelease-1>', Files.load_selected_file)

editArea.bind('<KeyRelease>', Files.changes)

root.bind('<Command-r>', Others.execute)
root.bind('<Command-s>', Files.SaveFile)
root.bind('<Command-l>', Json.LoadAndTestData)
root.bind("<Command-g>", ButtonActions.OpenGreen)
root.bind("<Command-b>", ButtonActions.OpenBlue)
root.bind("<Command-j>", Settings.JsonFileDirecotry)
editArea.bind("<Command-BackSpace>", TextFormating.DeleteLine)
editArea.bind("<Command-z>", TextFormating.Undo)
editArea.bind("<Tab>", TextFormating.InstertTab)

  # Přednastavený příkaz


root.mainloop()