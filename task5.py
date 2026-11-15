# Task 5 
import csv
import os
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from unittest import mock
from task1 import SmartDevice, SmartPlug
from task2 import SmartDoor, SmartAirFryer
from task3 import SmartHome, CapacityError
from task4 import SmartHomeApp as _LayoutApp, BG, TEXT

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "homes_data.csv")
CSV_FIELDS = ["home", "max_items", "type", "switched_on", "option"]

# pop up windows
class OptionInput(tk.Frame):
    def __init__(self, parent, device_cls, current=None):
        super().__init__(parent, bg=BG)
        self.device_cls = device_cls
        label = f"{device_cls.OPTION_LABEL} {device_cls.OPTION_HINT}".strip() + ":"
        tk.Label(self, text=label, bg=BG, fg=TEXT, font=("Segoe UI", 10)).pack(anchor="w", pady=4)

        if device_cls.CHOICES is None:
            self._text = tk.StringVar(value="" if current is None else str(current))
            tk.Entry(self, textvariable=self._text, width=20, bg="#313244", fg=TEXT,
                     insertbackground=TEXT, relief="flat",
                     font=("Segoe UI", 10)).pack(anchor="w")
        else:
            start = device_cls.CHOICES.index(current) if current in device_cls.CHOICES else 0
            self._index = tk.IntVar(value=start)
            for position, choice in enumerate(device_cls.CHOICES):
                tk.Radiobutton(self, text=str(choice), variable=self._index, value=position,
                               bg=BG, fg=TEXT, selectcolor="#313244",
                               activebackground=BG).pack(anchor="w")

    def get_value(self):
        if self.device_cls.CHOICES is None:
            return self.device_cls.parse_option(self._text.get())
        return self.device_cls.CHOICES[self._index.get()]

    def set_value(self, value):
        if self.device_cls.CHOICES is None:
            self._text.set(str(value))
        else:
            self._index.set(self.device_cls.CHOICES.index(value))

def _make_dialog(parent, title):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.configure(bg=BG)
    dialog.resizable(False, False)
    dialog.transient(parent)
    return dialog

def _dialog_buttons(dialog, ok_text, ok_command):
    row = tk.Frame(dialog, bg=BG)
    row.pack(pady=10)
    tk.Button(row, text=ok_text, command=ok_command, bg="#89b4fa", fg=BG, relief="flat",
              font=("Segoe UI", 10, "bold"), padx=10).pack(side="left", padx=6)
    tk.Button(row, text="Cancel", command=dialog.destroy, bg="#45475a", fg=TEXT,
              relief="flat", font=("Segoe UI", 10), padx=10).pack(side="left", padx=6)

class DeviceEditDialog(tk.Toplevel):
    def __init__(self, parent, device, on_confirm):
        super().__init__(parent)
        self.device = device
        self.on_confirm = on_confirm
        self.title("Edit Device")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)

        tk.Label(self, text=f"Editing {type(device).__name__}", bg=BG, fg="#89b4fa",
                 font=("Segoe UI", 11, "bold")).pack(padx=14, pady=8)
        self.option_input = OptionInput(self, type(device), device.option)
        self.option_input.pack(padx=14, pady=4, anchor="w")
        _dialog_buttons(self, "Confirm", self._confirm)

        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    def _confirm(self):
        try:
            self.device.option = self.option_input.get_value()
        except (ValueError, TypeError) as e:
            messagebox.showerror("Validation Error", str(e), parent=self)
            return
        self.on_confirm()
        self.destroy()


class AddDeviceDialog(tk.Toplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.types = SmartDevice.registered_types()
        self.title("Add Device")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(parent)

        tk.Label(self, text="Device type:", bg=BG, fg=TEXT,
                 font=("Segoe UI", 10)).pack(padx=14, pady=(10, 2), anchor="w")
        self.type_var = tk.StringVar(value=next(iter(self.types)))
        for name in self.types:
            tk.Radiobutton(self, text=name, variable=self.type_var, value=name,
                           command=self._show_option, bg=BG, fg=TEXT, selectcolor="#313244",
                           activebackground=BG).pack(anchor="w", padx=24)

        self._option_holder = tk.Frame(self, bg=BG)
        self._option_holder.pack(padx=14, pady=8, anchor="w")
        self.option_input = None
        self._show_option()
        _dialog_buttons(self, "Add", self._add)

        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    def _show_option(self):
        for widget in self._option_holder.winfo_children():
            widget.destroy()
        device_cls = self.types[self.type_var.get()]
        default = device_cls.create_default()
        self.option_input = OptionInput(self._option_holder, device_cls, default.option)
        self.option_input.pack(anchor="w")

    def _add(self):
        device_cls = self.types[self.type_var.get()]
        try:
            device = device_cls.create_default()
            device.option = self.option_input.get_value()
        except (ValueError, TypeError) as e:
            messagebox.showerror("Validation Error", str(e), parent=self)
            return
        self.on_confirm(device)
        self.destroy()

# task 5 
class SmartHomeApp(_LayoutApp):
    def _toggle_device(self, index):
        try:
            self.home.toggle_device(index)
        except IndexError as e:
            messagebox.showerror("Error", str(e), parent=self.root)
        self._refresh()

    def _edit_device(self, index):
        try:
            device = self.home.get_device(index)
        except IndexError as e:
            messagebox.showerror("Error", str(e), parent=self.root)
            return
        DeviceEditDialog(self.root, device, self._refresh)

    def _delete_device(self, index):
        if not messagebox.askyesno("Delete Device", f"Remove device {index + 1}?",
                                   parent=self.root):
            return
        try:
            self.home.remove_device(index)
        except IndexError as e:
            messagebox.showerror("Error", str(e), parent=self.root)
        self._refresh()

    def _add_device(self):
        def on_confirm(device):
            try:
                self.home.add_device(device)
            except CapacityError as e:
                messagebox.showerror("Capacity Error", str(e), parent=self.root)
            self._refresh()

        AddDeviceDialog(self.root, on_confirm)

    def _turn_all_on(self):
        self.home.switch_all_on()
        self._refresh()

    def _turn_all_off(self):
        self.home.switch_all_off()
        self._refresh()
# challenge 
def save_homes(homes, path=SAVE_FILE):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_FIELDS)
        for name, home in homes.items():
            if home.device_count() == 0:
                # keep homes without devices by writing a row with no device.
                writer.writerow([name, home.max_items, "", "", ""])
            for i in range(home.device_count()):
                device = home.get_device(i)
                writer.writerow([name, home.max_items, type(device).__name__,
                                 device.switched_on, device.option])

def _row_to_device(row):
    device_cls = SmartDevice.registered_types()[row["type"]]
    device = device_cls.create_default()
    device.option = device_cls.parse_option(row["option"])
    device.switched_on = row["switched_on"] == "True"
    return device

def load_homes(path=SAVE_FILE):
    if not os.path.exists(path):
        return None
    homes = {}
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != CSV_FIELDS:
                return None
            for row in reader:
                name = row["home"]
                if name not in homes:
                    homes[name] = SmartHome(int(row["max_items"]))
                if row["type"]:
                    homes[name].add_device(_row_to_device(row))
    except (csv.Error, KeyError, ValueError, TypeError, CapacityError):
        return None
    return homes

class SmartHomesApp:
    def __init__(self, save_path=SAVE_FILE):
        self.save_path = save_path
        self.homes = {}
        self._windows = {}      
        self._load_or_default()

        self.root = tk.Tk()
        self.root.title("Smart Homes Manager")
        self.root.configure(bg=BG)
        self.root.minsize(700, 480)
        w, h = 820, 580
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self._build_ui()
        self._refresh_homes()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_or_default(self):
        loaded = load_homes(self.save_path)
        if loaded is not None:
            self.homes = loaded
            return
        home = SmartHome()
        home.add_device(SmartPlug(45))
        home.add_device(SmartDoor())
        home.add_device(SmartAirFryer())
        self.homes["Home 1"] = home

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#181825", pady=14)
        header.pack(fill="x")
        tk.Label(header, text="Smart Homes Manager", bg="#181825", fg="#89b4fa",
                 font=("Segoe UI", 16, "bold")).pack()

        top = tk.Frame(self.root, bg=BG, pady=6)
        top.pack(fill="x", padx=16)
        style = dict(font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5,
                     cursor="hand2", fg=BG)
        for text, colour, command in (("Add Home", "#a6e3a1", self._add_home),
                                      ("Rename Home", "#f9e2af", self._rename_home),
                                      ("Remove Home", "#f38ba8", self._remove_home),
                                      ("Open Home", "#89b4fa", self._open_home)):
            tk.Button(top, text=text, command=command, bg=colour, **style).pack(side="left", padx=4)
        tk.Label(top, text="(double-click a home to open it)", bg=BG, fg="#6c7086",
                 font=("Segoe UI", 8)).pack(side="left", padx=6)

        tk.Frame(self.root, bg="#313244", height=1).pack(fill="x", padx=16, pady=4)

        self._listbox = tk.Listbox(self.root, bg="#24273a", fg=TEXT, font=("Segoe UI", 10),
                                   selectbackground="#313244", selectforeground="#89b4fa",
                                   relief="flat", bd=0, activestyle="none",
                                   exportselection=False)
        self._listbox.pack(fill="both", expand=True, padx=16, pady=4)
        self._listbox.bind("<Double-1>", lambda e: self._open_home())

    def _refresh_homes(self):
        selected = self._selected_name()
        self._listbox.delete(0, tk.END)
        for name, home in self.homes.items():
            self._listbox.insert(
                tk.END,
                f"  {name}   |   {home.device_count()} device(s)   |   {home.count_on()} on"
            )
        if selected in self.homes:
            self._listbox.selection_set(list(self.homes).index(selected))

    def _selected_name(self):
        selection = self._listbox.curselection()
        names = list(self.homes)
        if not selection or selection[0] >= len(names):
            return None
        return names[selection[0]]

    def _ask_name(self, title, prompt, initial=""):
        name = simpledialog.askstring(title, prompt, initialvalue=initial, parent=self.root)
        if name is None:
            return None
        name = name.strip()
        if not name:
            messagebox.showerror("Error", "Home name cannot be empty.", parent=self.root)
            return None
        if name != initial and name in self.homes:
            messagebox.showerror("Error", f"A home named '{name}' already exists.",
                                 parent=self.root)
            return None
        return name

    def _add_home(self):
        name = self._ask_name("New Home", "Enter a name for the new home:")
        if name:
            self.homes[name] = SmartHome()
            self._refresh_homes()

    def _rename_home(self):
        old = self._selected_name()
        if old is None:
            messagebox.showinfo("Select Home", "Please select a home first.", parent=self.root)
            return
        new = self._ask_name("Rename Home", "Enter a new name:", initial=old)
        if not new or new == old:
            return
        self.homes = {(new if n == old else n): h for n, h in self.homes.items()}
        window = self._windows.get(self.homes[new])
        if window:
            window.root.title(f"{new} - Device Manager")
            window._title_label.config(text=new)
        self._refresh_homes()

    def _remove_home(self):
        name = self._selected_name()
        if name is None:
            messagebox.showinfo("Select Home", "Please select a home first.", parent=self.root)
            return
        if messagebox.askyesno("Remove Home", f"Remove '{name}' and all its devices?",
                               parent=self.root):
            self._close_home_window(self.homes[name])
            del self.homes[name]
            self._refresh_homes()

    def _open_home(self):
        name = self._selected_name()
        if name is None:
            messagebox.showinfo("Select Home", "Please select a home first.", parent=self.root)
            return
        home = self.homes[name]
        if home in self._windows:
            self._windows[home].root.lift()
            return
        window = SmartHomeApp(home, master=self.root, title=name,
                              on_change=self._refresh_homes)
        window.root.title(f"{name} - Device Manager")
        window.root.protocol("WM_DELETE_WINDOW", lambda: self._close_home_window(home))
        self._windows[home] = window

    def _close_home_window(self, home):
        window = self._windows.pop(home, None)
        if window:
            window.root.destroy()
        self._refresh_homes()

    def _on_close(self):
        # save everything when the user exits.
        try:
            save_homes(self.homes, self.save_path)
        except OSError as e:
            messagebox.showwarning("Save Error", f"Could not save homes: {e}", parent=self.root)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

# tests
def _all_buttons(widget):
    found = []
    for child in widget.winfo_children():
        if isinstance(child, tk.Button):
            found.append(child)
        found.extend(_all_buttons(child))
    return found

def _click(app, text, nth=0):
    buttons = [b for b in _all_buttons(app.root) if b.cget("text") == text]
    buttons[nth].invoke()
    app.root.update()
    time.sleep(0.4)


def _when_dialog_opens(app, dialog_cls, action, delay=250):
    def run():
        dialog = [w for w in app.root.winfo_children() if isinstance(w, dialog_cls)][0]
        action(dialog)
    app.root.after(delay, run)


def test_smart_home_system(keep_open=True):
    print("=" * 50)
    print("TEST: SmartHomeApp interactivity (task 5)")
    print("=" * 50)

    home = SmartHome(max_items=4)
    home.add_device(SmartPlug(45))
    home.add_device(SmartDoor())
    home.add_device(SmartAirFryer())
    print(home)

    app = SmartHomeApp(home)
    app.root.update()

    def shown_cards():
        return [b for b in _all_buttons(app._device_frame) if b.cget("text") == "Delete"]

    _click(app, "Turn on all")
    assert all(home.get_device(i).switched_on for i in range(3))
    print("Turn on all: OK")
    _click(app, "Turn off all")
    assert not any(home.get_device(i).switched_on for i in range(3))
    print("Turn off all: OK")

    for i in range(3):
        _click(app, "Toggle", i)
        assert home.get_device(i).switched_on
    print("Toggle on every device: OK")

    # delete asks for confirmation, answer yes.
    with mock.patch.object(messagebox, "askyesno", return_value=True):
        _click(app, "Delete", 1)
    assert home.device_count() == 2 and len(shown_cards()) == 2
    assert not any(isinstance(home.get_device(i), SmartDoor) for i in range(2))
    print("Delete: OK, the GUI shows", len(shown_cards()), "devices")

    errors = []

    def edit_plug(dialog):
        dialog.option_input.set_value("999")
        with mock.patch.object(messagebox, "showerror", side_effect=lambda t, m, **k: errors.append(m)):
            dialog._confirm()
        assert dialog.winfo_exists()
        dialog.option_input.set_value("99")
        dialog._confirm()

    _when_dialog_opens(app, DeviceEditDialog, edit_plug)
    _click(app, "Edit", 0)
    assert home.get_device(0).consumption_rate == 99 and errors
    print("Edit: OK, invalid value refused:", errors[0])

    # edit the air fryer.
    _when_dialog_opens(app, DeviceEditDialog,
                       lambda d: (d.option_input.set_value("Crispy"), d._confirm()))
    _click(app, "Edit", 1)
    assert home.get_device(1).cook_mode == "Crispy"
    print("Edit air fryer: OK")

    def add_door(dialog):
        dialog.type_var.set("SmartDoor")
        dialog._show_option()
        dialog.option_input.set_value(False)
        dialog._add()

    _when_dialog_opens(app, AddDeviceDialog, add_door)
    _click(app, "Add")
    assert home.device_count() == 3 and home.get_device(2).locked is False
    assert len(shown_cards()) == 3
    print("Add: OK, the GUI shows", len(shown_cards()), "devices")

    _when_dialog_opens(app, AddDeviceDialog, lambda d: (d.option_input.set_value(10), d._add()))
    _click(app, "Add")
    assert home.device_count() == 4
    with mock.patch.object(messagebox, "showerror", side_effect=lambda t, m, **k: errors.append(m)):
        _when_dialog_opens(app, AddDeviceDialog, lambda d: d._add())
        _click(app, "Add")
    assert home.device_count() == 4
    print("Capacity limit in the GUI: OK")

    print("Final state:")
    print(home)
    print()
    if keep_open:
        print("Window left open to look at - close it to continue.")
        app.run()
    else:
        app.root.destroy()

def test_smart_homes():
    import tempfile
    print("=" * 50)
    print("TEST: SmartHomes (challenge)")
    print("=" * 50)

    homes = {}
    homes["Flat"] = SmartHome()
    homes["Flat"].add_device(SmartPlug(60))
    homes["Flat"].add_device(SmartDoor())
    homes["Flat"].get_device(0).toggle_switch()
    homes["Cabin, North"] = SmartHome(max_items=4)       
    homes["Cabin, North"].add_device(SmartAirFryer())
    homes["Cabin, North"].get_device(0).cook_mode = "Crispy"
    homes["Empty"] = SmartHome()
    print("Added homes:", list(homes))
    print("Retrieved Flat:")
    print(homes["Flat"])

    folder = tempfile.mkdtemp()
    path = os.path.join(folder, "test_homes.csv")
    save_homes(homes, path)
    loaded = load_homes(path)
    assert list(loaded) == list(homes)
    for name in homes:
        assert str(loaded[name]) == str(homes[name]), name
        assert loaded[name].max_items == homes[name].max_items
    print("Saved and reloaded homes match the originals.")

    del loaded["Flat"]
    assert "Flat" not in loaded
    print("Removed Flat, homes left:", list(loaded))

    save_homes({}, path)
    assert load_homes(path) == {}
    print("Removing every home is remembered after a reload.")

    with open(path, "w", encoding="utf-8") as f:
        f.write("this is not a homes file")
    assert load_homes(path) is None
    assert load_homes(os.path.join(folder, "missing.csv")) is None
    print("Corrupt and missing files are handled.")

    os.remove(path)
    os.rmdir(folder)
    print()

if __name__ == "__main__":
    SmartHomesApp().run()
