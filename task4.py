# Task 4
import tkinter as tk
from tkinter import ttk
from task1 import SmartPlug
from task2 import SmartDoor, SmartAirFryer
from task3 import SmartHome

BG = "#1e1e2e"
BG_DARK = "#181825"
TEXT = "#cdd6f4"
MUTED = "#6c7086"

class SmartHomeApp:
    def __init__(self, home=None, master=None, title="Smart Home Manager", on_change=None):
        if home is None:
            home = SmartHome()
            home.add_device(SmartPlug(45))
            home.add_device(SmartDoor())
            home.add_device(SmartAirFryer())
        self.home = home
        self.on_change = on_change
        self.root = tk.Tk() if master is None else tk.Toplevel(master)
        self._setup_window(title)
        self._build_ui(title)
        self._refresh()

    def _setup_window(self, title):
        self.root.title(title)
        self.root.configure(bg=BG)
        self.root.minsize(620, 400)
        w, h = 760, 560
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self, title):
        header = tk.Frame(self.root, bg=BG_DARK, pady=14)
        header.pack(fill="x")
        self._title_label = tk.Label(header, text=title, bg=BG_DARK, fg="#89b4fa",
                                     font=("Segoe UI", 16, "bold"))
        self._title_label.pack()

        top = tk.Frame(self.root, bg=BG, pady=6)
        top.pack(fill="x", padx=16)
        style = dict(font=("Segoe UI", 9, "bold"), relief="flat",
                     padx=10, pady=5, cursor="hand2")
        tk.Button(top, text="Add", command=self._add_device,
                  bg="#a6e3a1", fg=BG, **style).pack(side="left", padx=4)
        tk.Button(top, text="Turn on all", command=self._turn_all_on,
                  bg="#89b4fa", fg=BG, **style).pack(side="left", padx=4)
        tk.Button(top, text="Turn off all", command=self._turn_all_off,
                  bg="#f38ba8", fg=BG, **style).pack(side="left", padx=4)
        self._count_label = tk.Label(top, bg=BG, fg=MUTED, font=("Segoe UI", 9))
        self._count_label.pack(side="right", padx=8)

        tk.Frame(self.root, bg="#313244", height=1).pack(fill="x", padx=16, pady=4)

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=16, pady=4)

        self._canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._device_frame = tk.Frame(self._canvas, bg=BG)
        self._canvas_window = self._canvas.create_window((0, 0), window=self._device_frame,
                                                         anchor="nw")
        self._device_frame.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        # only listen to the mouse wheel while the pointer is over the list.
        self._canvas.bind("<Enter>", self._bind_wheel)
        self._canvas.bind("<Leave>", self._unbind_wheel)

    def _on_frame_configure(self, event=None):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _bind_wheel(self, event=None):
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_wheel(self, event=None):
        self._canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        try:
            self._canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
        except tk.TclError:
            self._canvas.unbind_all("<MouseWheel>")

    def _refresh(self):
        for widget in self._device_frame.winfo_children():
            widget.destroy()

        count = self.home.device_count()
        self._count_label.config(text=f"{count} / {self.home.max_items} device(s)")

        if count == 0:
            tk.Label(self._device_frame, text="No devices yet. Click Add to begin.",
                     bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(pady=30)
        for index in range(count):
            self._build_device_row(index, self.home.get_device(index))

        if self.on_change:
            self.on_change()

    def _build_device_row(self, index, device):
        is_on = device.switched_on
        card_bg = "#313244" if is_on else "#24273a"
        accent = "#a6e3a1" if is_on else MUTED

        card = tk.Frame(self._device_frame, bg=card_bg,
                        highlightbackground="#45475a", highlightthickness=1)
        card.pack(fill="x", pady=4, padx=2)

        buttons = tk.Frame(card, bg=card_bg)
        buttons.pack(side="right", padx=12, pady=10)
        left = tk.Frame(card, bg=card_bg)
        left.pack(side="left", fill="both", expand=True, padx=12, pady=10)

        name_row = tk.Frame(left, bg=card_bg)
        name_row.pack(anchor="w")
        tk.Label(name_row, text=type(device).__name__, bg=card_bg, fg=TEXT,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        tk.Label(name_row, text="  [ON]" if is_on else "  [OFF]", bg=card_bg, fg=accent,
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(left, text=f"{device.OPTION_LABEL}: {device.option}", bg=card_bg,
                 fg="#a6adc8", font=("Segoe UI", 9), wraplength=380,
                 justify="left").pack(anchor="w", padx=4)

        style = dict(font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=3,
                     cursor="hand2", fg=BG)
        tk.Button(buttons, text="Toggle", bg="#f9e2af" if is_on else "#89b4fa",
                  command=lambda: self._toggle_device(index), **style).pack(side="left", padx=3)
        tk.Button(buttons, text="Edit", bg="#89dceb",
                  command=lambda: self._edit_device(index), **style).pack(side="left", padx=3)
        tk.Button(buttons, text="Delete", bg="#f38ba8",
                  command=lambda: self._delete_device(index), **style).pack(side="left", padx=3)

    # placeholders for task 4
    def _toggle_device(self, index):
        pass

    def _edit_device(self, index):
        pass

    def _delete_device(self, index):
        pass

    def _add_device(self):
        pass

    def _turn_all_on(self):
        pass

    def _turn_all_off(self):
        pass

    def run(self):
        self.root.mainloop()


def test_smart_home_system():
    print("=" * 50)
    print("TEST: SmartHomeApp layout (task 4)")
    print("=" * 50)
    home = SmartHome()
    home.add_device(SmartPlug(45))
    home.add_device(SmartDoor())
    home.add_device(SmartAirFryer())
    print(home)
    print()

    print("Opening the window - close it to continue.")
    SmartHomeApp(home).run()

if __name__ == "__main__":
    test_smart_home_system()
