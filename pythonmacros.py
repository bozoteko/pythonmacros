import tkinter as tk
from pynput.keyboard import Controller, Key, Listener
import threading
import time

class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro App")
        self.root.configure(bg="black")  # Set background color to black

        self.keyboard = Controller()

        self.macro_active = [False, False, False]  # List for each macro
        self.bind_keys = ['k', 'l', 'm']  # Default bind keys for each macro
        self.hold_durations = [0.4, 0.435, 0.62]  # Hold durations for each macro
        self.cooldown_duration = 2  # Cooldown period in seconds
        self.last_press_time = 0
        self.always_on_top = False

        self.top_label = tk.Label(root, text="Press 'k' to toggle Macro", bg="black", fg="white",
                                  font=("Helvetica", 12))
        self.top_label.pack(pady=10)

        self.bind_buttons = []
        self.toggle_buttons = []
        self.bind_key_buttons = []

        for i, duration in enumerate(self.hold_durations, start=1):
            macro_frame = tk.Frame(root, bg="black")
            macro_frame.pack(fill="x", pady=5)

            bind_button = tk.Button(macro_frame, text=f"Bind: {self.bind_keys[i - 1]}", bg="#9B59B6", fg="white",
                                    activebackground="#27AE60", highlightthickness=0,
                                    command=lambda i=i-1: self.change_bind_key(i))
            bind_button.pack(side="left", padx=5)
            self.bind_buttons.append(bind_button)

            button = tk.Button(macro_frame, text=f"Macro {i} OFF", bg="#3498DB", fg="white",
                               activebackground="#27AE60", highlightthickness=0,
                               command=lambda i=i-1: self.toggle_macro(i))
            button.pack(side="left")
            self.toggle_buttons.append(button)

        self.always_on_top_button = tk.Button(root, text="Always On Top: OFF", bg="#E67E22", fg="white",
                                              activebackground="#27AE60", highlightthickness=0,
                                              command=self.toggle_always_on_top)
        self.always_on_top_button.pack(pady=5)

        self.listener = Listener(on_release=self.on_release)
        self.listener.start()

        self.footer_label = tk.Label(root, text="Made by Teko", bg="black", fg="white")
        self.footer_label.pack(side="bottom", pady=5, padx=5)

    def toggle_macro(self, index):
        if self.macro_active[index]:
            self.macro_active[index] = False
            self.toggle_buttons[index].config(text=f"Macro {index+1} OFF", bg="#3498DB")
            self.update_top_label()
        else:
            self.macro_active[index] = True
            self.toggle_buttons[index].config(text=f"Macro {index+1} ON", bg="#27AE60")
            self.update_top_label()

    def change_bind_key(self, index):
        self.top_label.config(text=f"Press a new key to bind Macro {index + 1}...")
        self.root.bind("<Key>", lambda event, i=index: self.set_bind_key(event, i))

    def set_bind_key(self, event, index):
        self.bind_keys[index] = event.keysym
        self.bind_buttons[index].config(text=f"Bind: {self.bind_keys[index]}", bg="#9B59B6")
        self.top_label.config(text="Press 'k' to toggle Macro")
        self.root.unbind("<Key>")  # Unbind the temporary listener

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        if self.always_on_top:
            self.always_on_top_button.config(text="Always On Top: ON", bg="#27AE60")
        else:
            self.always_on_top_button.config(text="Always On Top: OFF", bg="#E67E22")

    def on_release(self, key):
        try:
            key_char = key.char.lower()  # Convert the key character to lowercase
            if key_char in self.bind_keys and any(self.macro_active) and self.can_press():
                index = self.bind_keys.index(key_char)
                for i, active in enumerate(self.macro_active):
                    if active and i == index:
                        self.run_macro(i)
        except AttributeError:
            pass

    def can_press(self):
        current_time = time.time()
        if current_time - self.last_press_time >= self.cooldown_duration:
            self.last_press_time = current_time
            return True
        return False

    def run_macro(self, index):
        self.keyboard.press('e')
        time.sleep(self.hold_durations[index])
        self.keyboard.release('e')

    def update_top_label(self):
        active_macros = [f"Macro {i+1}" for i, active in enumerate(self.macro_active) if active]
        if active_macros:
            self.top_label.config(text=f"Active Macros: {', '.join(active_macros)}")
        else:
            self.top_label.config(text="Press 'k' to toggle Macro")

def main():
    root = tk.Tk()
    root.geometry("250x200")  # Set window size
    app = MacroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
