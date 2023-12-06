import tkinter as tk
from tkinter import messagebox
import keyboard
import os
import json

class ProgramOpenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Opener")

        self.shortcuts = {}

        self.load_shortcuts()  # Load existing shortcuts from file
        self.create_widgets()

        # Bind a function to handle the window closing event
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Label and Entry for program path
        program_label = tk.Label(self.root, text="Program Path:")
        program_label.grid(row=0, column=0, sticky="e")

        self.program_entry = tk.Entry(self.root, width=30)
        self.program_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label and Entry for keyboard shortcut
        shortcut_label = tk.Label(self.root, text="Shortcut:")
        shortcut_label.grid(row=1, column=0, sticky="e")

        self.shortcut_entry = tk.Entry(self.root, width=30)
        self.shortcut_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button to set the shortcut
        set_button = tk.Button(self.root, text="Set Shortcut", command=self.set_shortcut)
        set_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Listbox to display shortcuts
        self.shortcuts_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=5, width=35)
        self.shortcuts_listbox.grid(row=3, column=0, columnspan=2, pady=10)

        # Button to remove selected shortcut
        remove_button = tk.Button(self.root, text="Remove Selected", command=self.remove_shortcut)
        remove_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Populate the listbox with existing shortcuts
        for shortcut in self.shortcuts:
            self.shortcuts_listbox.insert(tk.END, f"{shortcut}: {self.shortcuts[shortcut]}")

    def set_shortcut(self):
        program_path = self.program_entry.get()
        shortcut = self.shortcut_entry.get()

        if not program_path or not shortcut:
            messagebox.showwarning("Warning", "Please enter program path and shortcut.")
            return

        try:
            self.register_hotkey(shortcut, program_path)
            self.shortcuts_listbox.insert(tk.END, f"{shortcut}: {program_path}")
            self.save_shortcuts()  # Save shortcuts to file
            messagebox.showinfo("Success", f"Shortcut {shortcut} set for {program_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error setting shortcut: {str(e)}")

    def remove_shortcut(self):
        selected_index = self.shortcuts_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a shortcut to remove.")
            return

        selected_index = selected_index[0]
        selected_item = self.shortcuts_listbox.get(selected_index)
        shortcut = selected_item.split(":")[0].strip()

        try:
            keyboard.remove_hotkey(shortcut)
            del self.shortcuts[shortcut]
            self.shortcuts_listbox.delete(selected_index)
            self.save_shortcuts()  # Save shortcuts to file
            messagebox.showinfo("Success", f"Shortcut {shortcut} removed.")
        except Exception as e:
            messagebox.showerror("Error", f"Error removing shortcut: {str(e)}")

    def save_shortcuts(self):
        with open("shortcuts.json", "w") as file:
            json.dump(self.shortcuts, file)

    def load_shortcuts(self):
        try:
            with open("shortcuts.json", "r") as file:
                self.shortcuts = json.load(file)
                for shortcut, program_path in self.shortcuts.items():
                    keyboard.add_hotkey(shortcut, self.open_program, args=(program_path,))
        except FileNotFoundError:
            pass  # File doesn't exist yet, ignore

    def on_close(self):
        self.save_shortcuts()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramOpenerApp(root)
    root.mainloop()
