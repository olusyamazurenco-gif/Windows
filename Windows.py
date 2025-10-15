import tkinter as tk
from tkinter import messagebox, simpledialog
import time

# Виртуальная ФС
vfs = {
    "files": {
        "readme.txt": "Это виртуальная файловая система.\nДважды кликните файл чтобы открыть.",
        "notes.txt": "Заметки..."
    },
    "folders": ["Документы", "Картинки", "Музыка"]
}

class Loader(tk.Toplevel):
    def __init__(self, master, on_finish):
        super().__init__(master)
        self.on_finish = on_finish
        self.overrideredirect(True)
        self.geometry("200x100+{}+{}".format(
            self.winfo_screenwidth()//2 - 100,
            self.winfo_screenheight()//2 - 50
        ))
        self.label = tk.Label(self, text="", font=("Arial", 24))
        self.label.pack(expand=True)
        self.dots = 0
        self.after(300, self.animate)

    def animate(self):
        self.dots = (self.dots + 1) % 4
        self.label.config(text="." * self.dots)
        if self.dots != 0:
            self.after(300, self.animate)
        else:
            # один полный цикл закончился, показать рабочий стол
            self.destroy()
            self.on_finish()

# Notepad
class Notepad(tk.Toplevel):
    def __init__(self, master, filename=None):
        super().__init__(master)
        self.title(filename or "Новый документ.txt")
        self.geometry("600x400")
        self.filename = filename
        self.text = tk.Text(self)
        self.text.pack(expand=True, fill="both")
        save_btn = tk.Button(self, text="Сохранить", command=self.save)
        save_btn.pack()
        if filename in vfs["files"]:
            self.text.insert("1.0", vfs["files"][filename])

    def save(self):
        if not self.filename:
            name = simpledialog.askstring("Имя файла", "Введите имя файла (.txt):")
            if not name:
                return
            self.filename = name
            self.title(name)
        vfs["files"][self.filename] = self.text.get("1.0", "end-1c")
        messagebox.showinfo("Сохранено", f"{self.filename} сохранён в виртуальной ФС")

# Explorer
class Explorer(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Проводник")
        self.geometry("400x400")
        self.listbox = tk.Listbox(self)
        self.listbox.pack(expand=True, fill="both")
        self.refresh()
        self.listbox.bind("<Double-Button-1>", self.open_item)
        create_btn = tk.Button(self, text="Создать текстовый файл", command=self.create_file)
        create_btn.pack()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for f in vfs["folders"]:
            self.listbox.insert(tk.END, f"[Папка] {f}")
        for f in vfs["files"]:
            self.listbox.insert(tk.END, f)

    def open_item(self, event):
        selection = self.listbox.get(self.listbox.curselection())
        if selection.startswith("[Папка]"):
            messagebox.showinfo("Папка", f"Открыта виртуальная папка: {selection[8:]}")
        else:
            Notepad(self, selection)

    def create_file(self):
        name = simpledialog.askstring("Новый файл", "Имя файла (.txt):")
        if name:
            vfs["files"][name] = ""
            self.refresh()

# Desktop
class Desktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Windows Emulator")
        self.geometry("800x600")
        self.configure(bg="#4c66a4")
        self.icons = []
        self.taskbar = tk.Frame(self, bg="#222", height=36)
        self.taskbar.pack(side="bottom", fill="x")
        self.start_btn = tk.Button(self.taskbar, text="Start", command=self.toggle_start)
        self.start_btn.pack(side="left")
        self.clock_label = tk.Label(self.taskbar, bg="#222", fg="white")
        self.clock_label.pack(side="right")
        self.update_clock()
        self.start_menu = None
        self.create_icons()

    def update_clock(self):
        self.clock_label.config(text=time.strftime("%H:%M:%S"))
        self.after(1000, self.update_clock)

    def create_icons(self):
        apps = [
            ("Проводник", self.open_explorer),
            ("Блокнот", self.open_notepad),
        ]
        for i, (name, cb) in enumerate(apps):
            btn = tk.Button(self, text=name, width=12, height=4, command=cb)
            btn.place(x=20 + (i % 4) * 120, y=20 + (i // 4) * 120)
            self.icons.append(btn)

    def toggle_start(self):
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None
        else:
            self.start_menu = tk.Toplevel(self)
            self.start_menu.geometry("150x200+0+400")
            tk.Button(self.start_menu, text="Проводник", command=self.open_explorer).pack(fill="x")
            tk.Button(self.start_menu, text="Блокнот", command=self.open_notepad).pack(fill="x")
            tk.Button(self.start_menu, text="Выход", command=self.quit).pack(fill="x")

    def open_explorer(self):
        Explorer(self)

    def open_notepad(self):
        Notepad(self)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # скрыть главное окно
    def start_desktop():
        root.destroy()
        Desktop().mainloop()
    Loader(root, start_desktop)
    root.mainloop()
