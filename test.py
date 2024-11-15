import tkinter as tk
from tkinter import ttk

class TextEditorWithLineNumbers(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor with Line Numbers")
        self.geometry("800x600")
        
        # Frame for layout
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Line number text widget
        self.line_numbers = tk.Text(frame, width=5, padx=5, takefocus=0, border=0,
                                    background="#000000", state=tk.DISABLED)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Main text widget
        self.text_widget = tk.Text(frame, wrap=tk.NONE, undo=True)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self._on_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=lambda *args: self._scroll_sync(*args, scrollbar=scrollbar))
        
        # Event bindings
        self.text_widget.bind("<KeyRelease>", self._update_line_numbers)
        self.text_widget.bind("<ButtonRelease>", self._update_line_numbers)
        
        # Initial line numbers update
        self._update_line_numbers()
    
    def _on_scroll(self, *args):
        """Handle scrolling and update line numbers."""
        self.text_widget.yview(*args)
        self.line_numbers.yview(*args)
        self._update_line_numbers()
    
    def _scroll_sync(self, *args, scrollbar):
        """Synchronize the scrollbar and update line numbers."""
        scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])
        self._update_line_numbers()
    
    def _update_line_numbers(self, event=None):
        """Update the line numbers."""
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        
        # Get the index of the first visible line
        first_visible_line = int(self.text_widget.index("@0,0").split(".")[0])
        
        # Get the number of visible lines
        total_lines = int(self.text_widget.index("end-1c").split(".")[0])
        line_numbers_content = "\n".join(str(i) for i in range(first_visible_line, total_lines + 1))
        
        # Insert updated line numbers
        self.line_numbers.insert(1.0, line_numbers_content)
        self.line_numbers.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = TextEditorWithLineNumbers()
    app.mainloop()
