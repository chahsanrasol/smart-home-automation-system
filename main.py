import task4
import task5
from task1 import test_smart_plug
from task2 import test_custom_device
from task3 import test_smart_home

MENU = {
    "1": ("Task 1 - SmartPlug test", test_smart_plug),
    "2": ("Task 2 - custom devices test (SmartDoor, SmartAirFryer)", test_custom_device),
    "3": ("Task 3 - SmartHome test", test_smart_home),
    "4": ("Task 4 - GUI layout (opens a window)", task4.test_smart_home_system),
    "5": ("Task 5 - GUI interactivity test (opens a window)", task5.test_smart_home_system),
    "6": ("Challenge - SmartHomes test (add, remove, save, load)", task5.test_smart_homes),
    "7": ("Challenge - open the Smart Homes app (GUI)", lambda: task5.SmartHomesApp().run()),
}
def main():
    while True:
        print("\nAlikoti Smart Home - choose what to run:")
        for key, (label, _function) in MENU.items():
            print(f"  {key}. {label}")
        print("  q. Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            break
        if choice in MENU:
            MENU[choice][1]()
        else:
            print("Please choose one of the options above.")

if __name__ == "__main__":
    main()
