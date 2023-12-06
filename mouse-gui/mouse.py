import tkinter as tk
from tkinter import messagebox
import ctypes
from ctypes import byref
from ctypes.wintypes import DWORD


class MouseSettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Settings")

        # Create labels and entry widgets
        self.mouse_speed_label = tk.Label(root, text="Mouse Speed:")
        self.mouse_speed_entry = tk.Entry(root)
        self.double_click_speed_label = tk.Label(root, text="Double Click Speed:")
        self.double_click_speed_entry = tk.Entry(root)

        # Get original mouse settings
        self.original_mouse_speed = self.get_mouse_speed()
        self.original_double_click_speed = self.get_double_click_speed()

        # Set default values
        self.mouse_speed_entry.insert(0, str(self.original_mouse_speed))
        self.double_click_speed_entry.insert(0, str(self.original_double_click_speed))

        # Create Apply and Revert buttons
        self.apply_button = tk.Button(root, text="Apply", command=self.apply_settings)
        self.revert_button = tk.Button(root, text="Revert", command=self.revert_settings)

        # Grid layout
        self.mouse_speed_label.grid(row=0, column=0, padx=10, pady=5)
        self.mouse_speed_entry.grid(row=0, column=1, padx=10, pady=5)
        self.double_click_speed_label.grid(row=1, column=0, padx=10, pady=5)
        self.double_click_speed_entry.grid(row=1, column=1, padx=10, pady=5)
        self.apply_button.grid(row=2, column=0, pady=10)
        self.revert_button.grid(row=2, column=1, pady=10)

    def apply_settings(self):
        try:
            # Get values from entry widgets
            mouse_speed = int(self.mouse_speed_entry.get())
            double_click_speed = int(self.double_click_speed_entry.get())

            # Set mouse speed
            self.set_mouse_speed(mouse_speed)

            # Set double-click speed
            self.set_double_click_speed(double_click_speed)

            tk.messagebox.showinfo("Success", "Mouse settings applied successfully!")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter valid integer values.")

    def revert_settings(self):
        # Revert to original mouse settings before the program was executed
        self.set_mouse_speed(self.original_mouse_speed)
        self.set_double_click_speed(self.original_double_click_speed)

        # Update entry widgets
        self.mouse_speed_entry.delete(0, tk.END)
        self.mouse_speed_entry.insert(0, str(self.original_mouse_speed))

        self.double_click_speed_entry.delete(0, tk.END)
        self.double_click_speed_entry.insert(0, str(self.original_double_click_speed))

        tk.messagebox.showinfo("Reverted", "Mouse settings reverted to original values.")

    def get_mouse_speed(self):
        speed = DWORD()
        ctypes.windll.user32.SystemParametersInfoW(0x0070, 0, byref(speed), 0)  # SPI_GETMOUSESPEED
        return speed.value

    def set_mouse_speed(self, speed):
        SPI_SETMOUSESPEED = 0x0071
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETMOUSESPEED, 0, speed, 0)

    def get_double_click_speed(self):
        return ctypes.windll.user32.GetDoubleClickTime()

    def set_double_click_speed(self, speed):
        SPI_SETDOUBLECLICKTIME = 0x0020
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDOUBLECLICKTIME, speed, 0, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseSettingsApp(root)
    root.mainloop()