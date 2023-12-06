import tkinter as tk
import threading
import keyboard

class MacroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Macro Program")

        self.is_macro_executed = False

        tk.Label(master, text="Enter key to press:").pack()
        self.key_entry = tk.Entry(master)
        self.key_entry.pack()

        tk.Label(master, text="Enter macro keys (comma-separated):").pack()
        self.macro_entry = tk.Entry(master)
        self.macro_entry.pack()

        self.set_macro_button = tk.Button(master, text="Set Macro", command=self.set_macro)
        self.set_macro_button.pack()

        # Bind the window closing event to a method
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start the thread to run the macro
        self.macro_thread = threading.Thread(target=self.run_macro)
        self.macro_thread.start()

    def set_macro(self):
        key_to_press = self.key_entry.get()
        macro_keys = self.macro_entry.get().split(',')

        # Put the macro information in the queue
        self.macro_thread.key_to_press = key_to_press
        self.macro_thread.macro_keys = macro_keys

    def run_macro(self):
        while True:
            try:
                if hasattr(self.macro_thread, 'key_to_press') and hasattr(self.macro_thread, 'macro_keys'):
                    key_to_press = self.macro_thread.key_to_press
                    macro_keys = self.macro_thread.macro_keys

                    if keyboard.is_pressed(key_to_press) and not self.is_macro_executed:
                        for macro_key in macro_keys:
                            keyboard.press_and_release(macro_key)

                        self.is_macro_executed = True
                    elif not keyboard.is_pressed(key_to_press):
                        self.is_macro_executed = False

            except KeyboardInterrupt:
                break
            
    def on_close(self):
        # This method is called when the user tries to close the window
        self.master.destroy()
        self.macro_thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()
    