# Task 3 
from task1 import SmartDevice, SmartPlug
from task2 import SmartDoor, SmartAirFryer
class CapacityError(Exception):
    pass

class SmartHome:
    def __init__(self, max_items=10):
        if isinstance(max_items, bool) or not isinstance(max_items, int) or max_items < 1:
            raise ValueError("max_items must be a positive whole number")
        self._devices = []
        self.max_items = max_items

    def _check_index(self, index):
        if not isinstance(index, int) or not 0 <= index < len(self._devices):
            raise IndexError(f"Invalid device index: {index}")

    def add_device(self, device):
        if not isinstance(device, SmartDevice):
            raise TypeError("Only smart devices can be added to a SmartHome")
        if len(self._devices) >= self.max_items:
            raise CapacityError(
                f"Cannot add device: SmartHome is at maximum capacity ({self.max_items})"
            )
        self._devices.append(device)

    def get_device(self, index):
        self._check_index(index)
        return self._devices[index]

    def remove_device(self, index):
        self._check_index(index)
        self._devices.pop(index)

    def toggle_device(self, index):
        self.get_device(index).toggle_switch()

    def switch_all_on(self):
        for device in self._devices:
            device.switched_on = True

    def switch_all_off(self):
        for device in self._devices:
            device.switched_on = False

    def update_option(self, index, value):
        self.get_device(index).option = value

    def device_count(self):
        return len(self._devices)

    def count_on(self):
        return sum(1 for device in self._devices if device.switched_on)

    def __str__(self):
        lines = [f"SmartHome with {len(self._devices)} device(s):"]
        for number, device in enumerate(self._devices, start=1):
            lines.append(f"{number}- {device}")
        return "\n\n".join(lines)


def test_smart_home():
    print("=" * 50)
    print("TEST: SmartHome")
    print("=" * 50)

    plug = SmartPlug(45)
    door = SmartDoor()
    fryer = SmartAirFryer()

    home = SmartHome(max_items=3)
    for device in (plug, door, fryer):
        home.add_device(device)
    print(home)

    for i, expected in enumerate((plug, door, fryer)):
        assert home.get_device(i) is expected
        print(f"get_device({i}): {home.get_device(i)}")

    for i in range(3):
        home.toggle_device(i)
        print(f"After toggle_device({i}):")
        print(home)
    assert home.count_on() == 3

    home.switch_all_on()
    print("After switch_all_on:")
    print(home)
    home.switch_all_off()
    print("After switch_all_off:")
    print(home)
    assert home.count_on() == 0

    assert plug.consumption_rate == 45
    assert door.locked is True
    assert fryer.cook_mode == "Healthy"
    print("Option values unchanged after switching.")

    # max_items limit.
    try:
        home.add_device(SmartPlug(10))
        print("ERROR: capacity limit not enforced")
    except CapacityError as e:
        print(f"Excess device rejected: {e}")

    # valid updates for every device type.
    home.update_option(0, 100)
    home.update_option(1, False)
    home.update_option(2, "Defrost")
    assert plug.consumption_rate == 100
    assert door.locked is False
    assert fryer.cook_mode == "Defrost"
    print("After valid update_option calls:")
    print(home)

    # invalid updates
    bad_updates = [(0, 200), (0, -1), (0, "abc"),
                   (1, "yes"), (1, 1),
                   (2, "Bake"), (2, 5)]
    for index, bad in bad_updates:
        try:
            home.update_option(index, bad)
            print(f"ERROR: update_option({index}, {bad!r}) should fail")
        except (ValueError, TypeError) as e:
            print(f"Rejected update_option({index}, {bad!r}): {e}")
    assert plug.consumption_rate == 100
    assert door.locked is False
    assert fryer.cook_mode == "Defrost"

    home.remove_device(1)
    print("After remove_device(1):")
    print(home)
    for bad_idx in (-1, 2, 10):
        try:
            home.remove_device(bad_idx)
            print(f"ERROR: remove_device({bad_idx}) should fail")
        except IndexError as e:
            print(f"Rejected remove_device({bad_idx}): {e}")
    assert home.device_count() == 2

    print("Final state:")
    print(home)
    print()

if __name__ == "__main__":
    test_smart_home()
