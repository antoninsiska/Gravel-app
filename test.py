import asyncio
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

class CommandRunnerApp:
    def __init__(self, command="ping -c 4 google.com"):
        # Inicializace asyncio smyčky
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_asyncio_loop, args=(self.loop,), daemon=True)
        self.thread.start()

        # Tkinter okno pro hlavní aplikaci (root)
        self.root = tk.Tk()
        self.root.title("Command Runner")

        # Tento příkaz je předem nastaven
        self.command = command

        # Vytvoření widgetu pro zobrazení výstupu příkazu
        self.output_widget = ScrolledText(self.root, height=20, width=80)
        self.output_widget.pack(padx=10, pady=10)

        # Spuštění příkazu ihned při startu
        self.start_command(self.command)

    def start_command(self, command):
        # Spustí příkaz asynchronně a zobrazuje výstup v hlavním okně
        asyncio.run_coroutine_threadsafe(self.run_command(command), self.loop)

    async def run_command(self, command):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Čtení výstupu
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            self.output_widget.insert(tk.END, line.decode())
            self.output_widget.see(tk.END)

        await process.wait()
        self.output_widget.insert(tk.END, f"\nProcess finished with code {process.returncode}\n")

    def start_asyncio_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def run_app(self):
        # Spuštění hlavní Tkinter smyčky
        self.root.mainloop()

# Spuštění aplikace s předem definovaným příkazem
if __name__ == "__main__":
    app = CommandRunnerApp(command="ping -c 4 google.com")  # Přednastavený příkaz
    app.run_app()