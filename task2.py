# Task 2 - 
from task1 import SmartDevice
class SmartDoor(SmartDevice):
    OPTION_NAME = "locked"
    OPTION_LABEL = "Locked"
    CHOICES = (True, False)

    def __init__(self):
        super().__init__()
        self.locked = True

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        if not isinstance(value, bool):
            raise TypeError("locked must be a Boolean value")
        self._locked = value

    def __str__(self):
        return f"SmartDoor is {self._state()} with a locked value of {self.locked}"


class SmartAirFryer(SmartDevice):
    OPTION_NAME = "cook_mode"
    OPTION_LABEL = "Cook Mode"
    VALID_MODES = ("Healthy", "Defrost", "Crispy")
    CHOICES = VALID_MODES

    def __init__(self):
        super().__init__()
        self.cook_mode = "Healthy"

    @property
    def cook_mode(self):
        return self._cook_mode

    @cook_mode.setter
    def cook_mode(self, value):
        if value not in self.VALID_MODES:
            raise ValueError(f"cook_mode must be one of {self.VALID_MODES}")
        self._cook_mode = value

    def __str__(self):
        return f"SmartAirFryer is {self._state()} with a cook_mode value of {self.cook_mode}"

def test_custom_device():
    print("=" * 50)
    print("TEST: Custom Devices")
    print("=" * 50)

    door = SmartDoor()
    fryer = SmartAirFryer()
    print(door)
    print(fryer)

    # defaults from table 1
    assert door.locked is True and door.switched_on is False
    assert fryer.cook_mode == "Healthy" and fryer.switched_on is False
    print("Default values verified.")

    door.toggle_switch()
    fryer.toggle_switch()
    print(door)
    print(fryer)
    assert door.switched_on and fryer.switched_on

    door.locked = False
    fryer.cook_mode = "Crispy"
    print(door)
    print(fryer)
    assert door.locked is False and fryer.cook_mode == "Crispy"

    for bad_locked in ("True", "yes", 1, 0, None):
        try:
            door.locked = bad_locked
            print(f"ERROR: locked={bad_locked!r} should have been rejected")
        except TypeError as e:
            print(f"Rejected locked={bad_locked!r}: {e}")
    assert door.locked is False

    for bad_mode in ("Bake", "raw", "", 42):
        try:
            fryer.cook_mode = bad_mode
            print(f"ERROR: cook_mode={bad_mode!r} should have been rejected")
        except ValueError as e:
            print(f"Rejected cook_mode={bad_mode!r}: {e}")
    assert fryer.cook_mode == "Crispy"

    # toggling back off
    door.toggle_switch()
    assert door.switched_on is False
    print()

if __name__ == "__main__":
    test_custom_device()
