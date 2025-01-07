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
import markdown
from tkhtmlview import HTMLLabel
from tkinter import messagebox as mbox
from tklinenums import TkLineNumbers
import json
from tkinter.scrolledtext import ScrolledText
import threading
import asyncio
import sys
import time
import logging
import objc
from Cocoa import (
    NSApplication,
    NSStatusBar,
    NSImage,
    NSMenu,
    NSMenuItem,
    NSObject,
)
from PyObjCTools.AppHelper import runEventLoop
first = True


logging.basicConfig(
    filename='/Users/antoninsiska/Documents/Projekty/Gravel-app/app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')


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

    library = ["pybricks", "pybricksdev"]

    libraryMissing = False
    pythonMissing = False
    pipMissing = False    

    rides = {
        "Red": "demo.py",
        "Green": "None",
        "Black": "None",
        "Pink": "None",
        "Purple": "None",
        "Yellow": "None",
        "Blue": "None"

    }

    usrsandpass = {
        "Tonda": "6996",
        "Matěj": "Skibidi",
    }
    # Načtení obrázku
    image_path = '/Users/antoninsiska/Documents/Projekty/Gravel-app/image.jpeg'

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

    edit_area_frame = tk.Frame(root)
    edit_area_frame.pack(fill=tk.Y, side=tk.RIGHT, expand=1)

    # Make the Text Widget
    editArea = Text(
        edit_area_frame,
        background=background,
        foreground=normal,
        insertbackground=normal,
        relief=FLAT,
        borderwidth=30,
        font=font,
        undo=True,
        height=39
    )


    # Vytvoření listboxu pro soubory
    

    # Přesunutí editArea na správné místo pomocí grid
    #editArea.pack(side=RIGHT, fill=BOTH, expand=1)
    editArea.grid(row = 0, column = 0, sticky = W, pady = 2)

    # Nastavení mřížky na pružné roztažení
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)


    
    

    file_list_frame = tk.Frame(root, bg="#2d2d2d")
    file_list_frame.pack(side=tk.LEFT, fill=tk.Y, expand=1)

    file_list = tk.Listbox(file_list_frame, bg="#333333", fg="white", selectbackground="#444444")
    file_list.pack(fill=tk.BOTH, expand=1)  

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

        logging.info("Opening file")

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
        if Contstants.file_list.curselection():
            selected_file = Contstants.file_list.get(Contstants.file_list.curselection())
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
        logging.info("Loading files")

        # Definice file_list
        Contstants.file_list.delete(0, tk.END)
        try:
            for file_name in os.listdir(directory):
                if file_name.endswith(".py") and file_name in Contstants.specific_file_names:
                    Contstants.file_list.insert(tk.END, file_name)
        except FileNotFoundError:
            messagebox.showerror("Error", "Directory not found!")


    def SaveFile(event=None):
        logging.info("Saving file")

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
        
        logging.info("Checking for changes")

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
        logging.info("Opening settings")
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
        logging.info("Opening hub name settings")
        newHubName = simpledialog.askstring("Hub name", "Enter new hub name:", initialvalue=Contstants.hubName)
        if newHubName:
            Contstants.hubName = newHubName
        MenuBar.Update()
        logging.info("Hub name changed")

    def PybricksDirectorySettigns():
        global pybricksDirectory
        logging.info("Opening pybricks directory settings")
        newPybricksDirectory = simpledialog.askstring("Pybricks directory", "Enter pybricks directory:", initialvalue=Contstants.pybrikcsDirectory)
        if newPybricksDirectory:
            Contstants.pybrikcsDirectory = newPybricksDirectory
        logging.info("Pybricks directory changed")

    def DemoFileSettings():
        global demoFileName
        logging.info("Opening demo file settings")
        # Možnost výběru demo souboru
        demo_file_path = filedialog.askopenfilename(
            title="Select Demo File",
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*")),
            initialdir=Contstants.directory_path
        )
        if demo_file_path:
            Contstants.fileName = os.path.basename(demo_file_path)
        logging.info("Demo file changed")

    def ImageDirectorySettings():
        
        newImageDirectory = simpledialog.askstring("Image directory", "Enter image directory:", initialvalue="")
        if newImageDirectory:
            Contstants.imageDirectory = newImageDirectory

    def JsonFileDirecotry(event=False):
        
        logging.info("Opening json file directory settings")
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
        logging.info("Json file directory changed")
        


    def SetDeafult1():
        Contstants.hubName = "HUB_FLL08"
        MenuBar.Update()

    def SetDeafult2():
        Contstants.hubName = "HUB_FLL07"
        MenuBar.Update()

class GitHub:

   

    def GetCommit():
        logging.info("Opening commit")
        githubBool = True
        if githubBool:
            a = messagebox.askquestion("GitHub", "Opravdu cheš vytvořit commit")
            if a == "yes":
                commit = simpledialog.askstring("Commit message", "Enter commit message:")
                Others.VerifyCommand(["git", "add", "."], cwd=Contstants.directory_path)
                Others.VerifyCommand(['git', 'commit', '-m', commit], cwd=Contstants.directory_path)   
                Contstants.gitHubCommit = True
                MenuBar.Update()
                logging.info("Commit created")
     
        

    def Pull():
        a = messagebox.askquestion("GitHub", "Opravdu chceš vytvořit pull")
        if a == "yes":
            githubBool = Settings.SetGithub(ask=False)
            if githubBool:
                Others.VerifyCommand(['git', 'pull'])
                logging.info("Pull created")
        

    def Push():
        a = messagebox.askquestion("GitHub", "Opravdu chceš nahrát commit na github.")
        if a == "yes":
            Others.VerifyCommand(['git', 'push'], cwd=Contstants.directory_path)
            Contstants.gitHubCommit = False
            MenuBar.Update()
            logging.info("Push created")

class CMDViewer:
    def __init__(self, root, command):
        self.root = root
        self.loop = asyncio.new_event_loop()
        self.command = command

        # Uchování posledních tří řádků výstupu
        self.last_lines = deque(maxlen=3)
        self.output_lines = []  # List to store output lines

        # Spustí asyncio smyčku v samostatném vlákně
        self.thread = threading.Thread(target=self.start_asyncio_loop, args=(self.loop,), daemon=True)
        self.thread.start()

        # Automatické spuštění příkazu
        self.open_new_window(self.command)

    def open_new_window(self, command):

        logging.info(f"Opening new window for command: {command}")

        # Vytvoření nového okna
        self.new_window = Contstants.edit_area_frame
        #self.new_window.title(f"Command: {command}")

        self.output_widget = ScrolledText(self.new_window, height=26, width=120)
        #self.output_widget.pack(padx=10, pady=10)
        Contstants.editArea.config(height=20)
        self.output_widget.grid(row = 1, column = 0, sticky = W, pady = 2)
        

        # Spuštění příkazu asynchronně
        self.start_command(command, self.output_widget)

    def start_command(self, command, output_widget):
        logging.info(f"Running command: {command}")
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
        logging.info(f"Output: {text}")
        lines = text.splitlines()
        for line in lines:
            output_widget.insert(tk.END, line + '\n')
            output_widget.see(tk.END)
            self.output_lines.append(line)  # Append each line to the list
            self.last_lines.append(line.strip())
        print(self.output_lines)

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
        Contstants.editArea.config(height=39)

    def start_asyncio_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

class Others:

    def get_app_location():
        logging.info("Getting app location")
        if hasattr(sys, '_MEIPASS'):  # Pokud běžíte z balíčku PyInstaller
            # Vrátí cestu k balíčku .app
            return str(os.path.dirname(sys.executable))
        else:
            # Pokud aplikaci spouštíte přímo z vývojového prostředí (např. IDE)
            return str(os.getcwd())
    
    def LogIn():
        logging.info("Logging in")
        username = simpledialog.askstring("Username", "Please enter your username:")
        if username:
            Contstants.jsonFileName = (Others.get_app_location()) + "/dist/Gravel.app/" + username + ".json"
            Json.LoadAndTestData()
        else:
            messagebox.showwarning("Username", "No username entered.")


    

    def execute(event=None):
        global current_file
        logging.info("Executing program")
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
            CMDViewer(Contstants.editArea, command=f"cd {Contstants.directory_path} && {Contstants.pybrikcsDirectory} run ble -n {Contstants.hubName} {Contstants.fileName}")
            Contstants.editArea.grid(row = 0, column = 0, sticky = W, pady = 2)

            """Others.VerifyCommand(['sh', '-c', f'cd {Contstants.directory_path} && {Contstants.pybrikcsDirectory} run ble -n {Contstants.hubName} {Contstants.fileName}'])
        else:
            messagebox.showwarning("Warning", "No file opened.")"""


    def VerifyCommand(command:list, cwd=None):
        logging.info(f"Verifying command: {command}")
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

    def GetLocalTime():
        logging.info("Getting local time")
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time

class HelpWindow:
    # Markdown text
    def ShowMarkdown(markdown_text):


        # Převod Markdown na HTML
        html_text = markdown.markdown(markdown_text)
        print(html_text)
        # Vytvoření tkinter okna
        root = Toplevel(Contstants.root)
        root.title("Markdown v Tkinter")

        # Zobrazení HTML pomocí HTMLLabel
        html_label = HTMLLabel(root, html=html_text)
        html_label.pack(fill="both", expand=True, padx=10, pady=10)

    def OpenShortcutsHelp():
        markdown_text = "- **CMD + S** - Save \n - **CMD + R** - Run - otevře okno s terminálem a uloží a nahraje program do robota \n - **CMD + P** - Push - nahraje program na GitHub \n - **CMD + J** - otvře konfiguraci s nastevním aplikace \n - **CMD + L** -  otevře okno s výběrem konfigurace pro apliakaci \n - **CMD + Z** - krok zpět"
        HelpWindow.ShowMarkdown(markdown_text)

    def OpenEssentialsHelp():
        markdown_text = "# Základy\nAplikace složí k programování robota Gravel.\n## Programovací prostředí\nVpravo je velké textvé okno kam sepíše kód. Základní python funkce a naše všechyn funkce se zbarví jinou barvu pro lepší přehlednost. Vlevo je sloupeček rozdělen na dvě části, první část obsahuje seznam přístupných souborů. Přístupné soubory se nastavují v konfiguračním souboru. V druhé části se nachází důležité nebo základní funkce. Jsou tam tlačítka s commit message, tento nástrojvytvoří zprávu na github. Run uloží, nahraje program do robota a otvře okno terminálu s výstupem porgramu. Push nahrává zpravy na gitu na github. A markdown editor která se využije až v budoucnosti. Po zvoelní této možnosti je možné že aplikace spadne. Kousek nad talčítky je informační pás. První od spoda je ukazatel uložení soubru, pokud je to bílé tak soubor není uložen a pokud je to prázdné tak je soubor uložen. Nad tím je oznámení commitu (zda je nebo zda není). Výše je název hubu kam se bude nahrávat program. Název lze změnit v kartě settings Hub name a vybrat si. Náze lze nastavit i v konfiguračním souboru.\n## Konfigurační soubor\nKonfugrační soubr je soubr který nastavuje všechypotřebná nastvaení. Při jeho změneě hrozí narušení porgramu nebo aplikace **NEUPRAVOVAT**. Konfigurační soubor je potřeba nastavit při každém zapnutí aplikace.\n## Na co si dávat POZOR\n1. Přístup k hlavním soubrům programu by jsi neměl mít přístup díky kofiguračnímu souboru, ale pokdu by se stalo že by se k nim povedlo dostat tak zásadně neupravovat. Může stát že robot kvůli úpravě nebude jezidt nebo nebude přesně. Potom je těžké úpravu najít a upravit.\n2. Na konfigurační soubor, nikdy neupravovoat, potom apliake nemůusí fungovat správně.\n## Tipy\nV kartě help lze najít cokoliv potřebného pro aovládání aplikace."
        HelpWindow.ShowMarkdown(markdown_text)

    def OpenDocumentation():
        markdown_text = "# Dokumentace\nToto obsahuje základní příkay potřebné pro pohyby robota\n## Straight()\nFunkce straight slouží k jízdě rovně, do závorek se píše vzdálenost v cm.\n## Turn()\nFunkce turn slouží k zatáčení, do závorek se vklládá ůhel na který se otočit\n## TurnTool()\nTrunTool slouží k pohybu motorů pro násatvce. Do závorek se vkládá úhel o kolik a rcyhlost + jakým motorem L/R v uzovkách"
        HelpWindow.ShowMarkdown(markdown_text)

class Json:
    
    def Load():
        try:
            with open(Contstants.jsonFileName, "r") as file:
                data = json.load(file)
        except:
            messagebox.showerror("JSON file", f"Bad Json file directory: {Contstants.jsonFileName}")
            print("Bad Json file directory")
            Settings.JsonFileDirecotry()
            Json.LoadAndTestData()

        Contstants.hubName = data['data'][0]['hubName']
        Contstants.pybrikcsDirectory = data['data'][0]['pybrikcsDirectory']
        Contstants.fileName = data['data'][0]['fileName']
        Contstants.directory_path = data['data'][0]['directoryPath']
        Contstants.rides = data['data'][0]['rides'][0]
        Contstants.specific_file_names = data['data'][0]['specificFileNames']
        Contstants.image_path = data['data'][0]['imagePath']
        logging.info("Loaded json data")
        
        
    
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
    controls_menu.add_command(label="Log in", command=Others.LogIn)
    


    rides_menu = Menu(menu_bar, tearoff=2)
    menu_bar.add_cascade(label="Rides", menu=rides_menu)
    rides_menu.add_command(label="Red", command=Rides.Red)
    rides_menu.add_command(label="Green", command=Rides.Green)
    rides_menu.add_command(label="Black", command=Rides.Black)
    rides_menu.add_command(label="Blue", command=Rides.Blue)
    rides_menu.add_command(label="Yellow", command=Rides.Yellow)
    rides_menu.add_command(label="Purlple", command=Rides.Purple)
    rides_menu.add_command(label="Pink", command=Rides.Pink)
    
    help_menu = Menu(menu_bar, tearoff=3)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Essentials", command=HelpWindow.OpenEssentialsHelp)
    help_menu.add_command(label="Keyboard shortcuts", command=HelpWindow.OpenShortcutsHelp)
    help_menu.add_command(label="Documentation", command=HelpWindow.OpenDocumentation)


    file_list_frame = Contstants.file_list_frame

    text1 = Label(file_list_frame, text=Contstants.hubName)
    text2 = Label(file_list_frame, text="nothing commited")
    text3 = Label(file_list_frame, text="[     ]")

    logging.info("Menu bar created")

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

        logging.info("Menu bar updated")


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

        logging.info("Markdown editor opened")

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


# Nastavení Tkinter
root = Contstants.root
root.geometry('1100x1000')
root.title("Gravel")

image_path = Contstants.image_path

img = Image.open(image_path)
img = img.resize((1000, 600))
img_tk = ImageTk.PhotoImage(img)

#Others.LogIn()
# Otevření okna s obrázkem
background_color = img.getpixel((0, 0))

file_list_frame = Contstants.file_list_frame
 
# Listbox for files
print("Test")

print("bef log")

print("aft log")   

print("Test")
logging.info("App started")

# Variable to track the currently opened file
current_file = None
editArea = Contstants.editArea
print("yview", editArea.yview())

# Add buttons below the file_list
button1 = tk.Button(file_list_frame, text="Commit message", command=GitHub.GetCommit)
button2 = tk.Button(file_list_frame, text="Run", command=Others.execute)
button3 = tk.Button(file_list_frame, text="Push", command=GitHub.Push)
button4 = tk.Button(file_list_frame, text="Markdown editor", command=Window)
button5 = tk.Button(file_list_frame, text="")
print("TEST")
logging.info("Initalized buttons")
print("TEST")
print(os.system("pwd"))

print("Directory path")

messagebox.showinfo("Info", str(os.getcwd()))

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

Contstants.file_list.bind('<ButtonRelease-1>', Files.load_selected_file)

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