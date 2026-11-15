# Task 1 - 
class SmartDevice:
    OPTION_NAME = None     
    OPTION_LABEL = ""     
    OPTION_HINT = ""      
    CHOICES = None          

    _registry = {}       

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        SmartDevice._registry[cls.__name__] = cls

    def __init__(self):
        self.switched_on = False

    @classmethod
    def registered_types(cls):
        return dict(SmartDevice._registry)

    @classmethod
    def create_default(cls):
        return cls()

    @classmethod
    def parse_option(cls, text):
        if cls.CHOICES is None:
            raise NotImplementedError("free text devices must override parse_option")
        for choice in cls.CHOICES:
            if str(choice) == str(text):
                return choice
        raise ValueError(f"'{text}' is not a valid {cls.OPTION_LABEL}")

    @property
    def option(self):
        return getattr(self, self.OPTION_NAME)

    @option.setter
    def option(self, value):
        setattr(self, self.OPTION_NAME, value)

    def toggle_switch(self):
        self.switched_on = not self.switched_on

    def _state(self):
        return "on" if self.switched_on else "off"


class SmartPlug(SmartDevice):
    OPTION_NAME = "consumption_rate"
    OPTION_LABEL = "Consumption Rate"
    OPTION_HINT = "(0-150 W)"
    MIN_RATE = 0
    MAX_RATE = 150

    def __init__(self, consumption_rate):
        super().__init__()
        self.consumption_rate = consumption_rate

    @classmethod
    def create_default(cls):
        return cls(cls.MIN_RATE)

    @classmethod
    def parse_option(cls, text):
        try:
            return int(str(text).strip())
        except ValueError:
            raise ValueError("Consumption rate must be a whole number.")

    @property
    def consumption_rate(self):
        return self._consumption_rate

    @consumption_rate.setter
    def consumption_rate(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("consumption_rate must be an integer")
        if not self.MIN_RATE <= value <= self.MAX_RATE:
            raise ValueError(
                f"consumption_rate must be between {self.MIN_RATE} and {self.MAX_RATE} inclusive"
            )
        self._consumption_rate = value

    def __str__(self):
        return f"SmartPlug is {self._state()} with a consumption rate of {self.consumption_rate}"


def test_smart_plug():
    print("=" * 50)
    print("TEST: SmartPlug")
    print("=" * 50)

    plug = SmartPlug(45)
    print(plug)
    assert plug.switched_on is False

    plug.toggle_switch()
    print(plug)
    assert plug.switched_on is True

    plug.consumption_rate = 75
    print(plug)
    assert plug.consumption_rate == 75

    plug.toggle_switch()
    print(plug)
    assert plug.switched_on is False

    for bad_rate in (-10, 200):
        try:
            plug.consumption_rate = bad_rate
            print(f"ERROR: {bad_rate} should have been rejected")
        except (ValueError, TypeError) as e:
            print(f"Invalid update prevented for {bad_rate}: {e}")
    assert plug.consumption_rate == 75
    print(plug)

    for bad_init in (-5, 160):
        try:
            SmartPlug(bad_init)
            print(f"ERROR: initialisation with {bad_init} should have been rejected")
        except (ValueError, TypeError) as e:
            print(f"Invalid initialisation blocked for {bad_init}: {e}")

    print()

if __name__ == "__main__":
    test_smart_plug()
