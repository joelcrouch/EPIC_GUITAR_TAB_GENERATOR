import tkinter as tk
from src.ui import TabGeneratorApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Guitar Tab Generator")
    app = TabGeneratorApp(root)
    root.mainloop()