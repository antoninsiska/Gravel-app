from tkinter import *
from tkinter import scrolledtext, messagebox, Listbox, simpledialog
import tkinter as tk
import ctypes
import re
import os
import subprocess

# Setup Tkinter
root = Tk()
root.geometry('1000x1000')
root.title("Gravel")
hubName = "HUB_FLL08"
pybrikcsDirectory = "/Library/Frameworks/Python.framework/Versions/3.12/bin/pybricksdev"
fileName = "main.py"
specific_file_names = ["demo.py", "demoRide.py", "testRide.py"]

githubString = "Off"
# Folder where files are saved
directory_path = "/Users/antoninsiska/Documents/fll"


# Menu
def open_settings():
    global directory_path, specific_file_names

    new_directory_path = simpledialog.askstring("Directory Path", "Enter new directory path:", initialvalue=directory_path)
    if new_directory_path:
        directory_path = new_directory_path

    new_file_names = simpledialog.askstring("Specific File Names", "Enter specific file names (comma separated):", initialvalue=", ".join(specific_file_names))
    if new_file_names:
        specific_file_names = [name.strip() for name in new_file_names.split(",")]

    load_files(directory_path)

def HubNameSettings():
    global hubName
    newHubName = simpledialog.askstring("Hub name", "Enter new hub name:", initialvalue=hubName)
    if newHubName:
        hubName = newHubName

def PybricksDirectorySettigns():
    global pybricksDirectory
    newPybricksDirectory = simpledialog.askstring("Pybricks directory", "Enter pybricks directory:", initialvalue=pybricksDirectory)
    if newPybricksDirectory:
        pybricksDirectory = newPybricksDirectory

def DemoFileSettings():
    global demoFileName
    newDemoFileName = simpledialog.askstring("Demo file", "Enter demo file name:", initialvalue=fileName)
    if newDemoFileName:
        fileName = newDemoFileName

def ImageDirectorySettings():
    global imageDirectory
    newImageDirectory = simpledialog.askstring("Image directory", "Enter image directory:", initialvalue="")
    if newImageDirectory:
        imageDirectory = newImageDirectory

def VerifyCommand(command:list):
    try:
        result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
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


def GetCommit():
    
    githubBool = SetGithub(ask=False)
    if githubBool:
        commit = simpledialog.askstring("Commit message", "Enter commit message:")
        VerifyCommand(["git", "add", "."])
        VerifyCommand(['git', 'commit', '-m', commit])
        VerifyCommand(['git', 'push'])
    else:
        messagebox.showwarning("GitHub control", "Bad password")
    

def Pull():
    githubBool = SetGithub(ask=False)
    if githubBool:
        VerifyCommand(['git', 'pull'])
    else:
        messagebox.showwarning("GitHub control", "Bad password")
    

def execute(event=None):
    global current_file

    messagebox.showinfo("Info", "Program se po kliknutí na OK nahraje a spustí.")

    if current_file:
        with open(current_file, 'w', encoding='utf-8') as f:
            f.write(editArea.get('1.0', END))
        
        VerifyCommand(['sh', '-c', f'cd {directory_path} && {pybrikcsDirectory} run ble -n {hubName} {fileName}'])
    else:
        messagebox.showwarning("Warning", "No file opened.")





def changes(event=None):
    global previousText

    if editArea.get('1.0', END) == previousText:
        return

    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)
            i += 1

    previousText = editArea.get('1.0', END) 

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

def load_selected_file(event=None):
    global current_file
    if file_list.curselection():
        selected_file = file_list.get(file_list.curselection())
        file_path = os.path.join(directory_path, selected_file)
        try:
            with open(file_path, "r") as file:
                content = file.read()
                editArea.delete('1.0', END)
                editArea.insert('1.0', content)
                current_file = file_path
                global previousText
                previousText = content
                changes()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")
    else:
        messagebox.showwarning("Warning", "No file selected.")

def load_files(directory):
    file_list.delete(0, tk.END)
    try:
        for file_name in os.listdir(directory):
            if file_name.endswith(".py") and file_name in specific_file_names:
                file_list.insert(tk.END, file_name)
    except FileNotFoundError:
        messagebox.showerror("Error", "Directory not found!")

previousText = ''

def SetGithub(ask = True):
    githubPass = simpledialog.askstring("Image directory", "Enter image directory:", initialvalue=githubString)

    if githubPass == "TondaFLL":
        return True
    else:
        return False



# Setup Menu Bar
menu_bar = Menu(root)
settings_menu = Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Edit Directory Path", command=open_settings)
settings_menu.add_command(label="Edit Specific File Names", command=open_settings)
settings_menu.add_command(label="Pybricks directory", command=PybricksDirectorySettigns)
settings_menu.add_command(label="Image directory", command=ImageDirectorySettings)
settings_menu.add_command(label="Hub name", command=HubNameSettings)
settings_menu.add_command(label="Demo file", command=DemoFileSettings)
settings_menu.add_command(label="Github", command=SetGithub)
menu_bar.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menu_bar)

controls_menu = Menu(menu_bar, tearoff=1)
menu_bar.add_cascade(label="Control", menu=controls_menu)
controls_menu.add_command(label="Upload and run", command=execute)
controls_menu.add_command(label="Create commit", command=GetCommit)
controls_menu.add_command(label="Pull", command=Pull)

file_list_frame = tk.Frame(root, bg="#2d2d2d", width=100)
file_list_frame.pack(side=tk.LEFT, fill=tk.Y)

# Listbox for files
file_list = tk.Listbox(file_list_frame, bg="#333333", fg="white", selectbackground="#444444")
file_list.pack(fill=tk.BOTH, expand=True)

# Variable to track the currently opened file
current_file = None





# Define colors for the various types of tokens
normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
commands = rgb((40, 135, 255))
nums = rgb((102, 133, 218))
lastColour = rgb((255, 135, 135))
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

# Define button actions
def button1_action():
    messagebox.showinfo("Button 1", "Button 1 was clicked!")

def button2_action():
    messagebox.showinfo("Button 2", "Button 2 was clicked!")

def button3_action():
    messagebox.showinfo("Button 3", "Button 3 was clicked!")

def button4_action():
    messagebox.showinfo("Button 4", "Button 4 was clicked!")

# Add buttons below the file_list
button1 = tk.Button(file_list_frame, text="Commit message", command=GetCommit)
button2 = tk.Button(file_list_frame, text="Pull", command=Pull)
button3 = tk.Button(file_list_frame, text="Get info")
button4 = tk.Button(file_list_frame, text="Button 4", command=button4_action)

button1.pack(fill=tk.X, padx=5, pady=2)
button2.pack(fill=tk.X, padx=5, pady=2)
button3.pack(fill=tk.X, padx=5, pady=2)
button4.pack(fill=tk.X, padx=5, pady=2)

load_files(directory_path)

file_list.bind('<ButtonRelease-1>', load_selected_file)
editArea.bind('<KeyRelease>', changes)
root.bind('<Command-r>', execute)

root.mainloop()