from enum import Enum

import os
import pandas as pd

class MainMenuOptions(Enum):
    AUTOMATIC_MEASUREMENT = 1
    MANUAL_MEASUREMENT = 2
    EXIT = 3

class MeasurementMenuOptions(Enum):
    NO_MEASUREMENT = 1
    MANUAL_VI = 2
    MANUAL_IV = 3
    AUTOMATIC_VI = 4
    AUTOMATIC_IV = 5
    AUTOMATIC_VT = 6
    AUTOMATIC_IT = 7

class CurrentScaleOptions(Enum):
    MILIAMPS = 1
    MICROAMPS = 2
    NANOAMPS = 3

class VoltageScaleOptions(Enum):
    VOLTS = 1
    MILIVOLTS = 2
    MICROVOLTS = 3

class SelectKeithley(Enum):
    ONE = 1
    TWO = 2
    BOTH = 3

class MenuController:
    def __init__(self):
        self.menus = {
            "main": {
                "title": "Select the ejecution mode",
                "options": {
                    MainMenuOptions.AUTOMATIC_MEASUREMENT.value: "Automatic Measurement",
                    MainMenuOptions.MANUAL_MEASUREMENT.value: "Manual Measurement",
                    MainMenuOptions.EXIT.value: "Exit the program",
                }
            },
            "select_keithleys": {
                "title": "Which keithley do you want to use?",
                "options": {
                    SelectKeithley.ONE.value: "Keithley 1",
                    SelectKeithley.TWO.value: "Keithley 2",
                    SelectKeithley.BOTH.value: "Both Keithleys",
                }
            },
            "measurement": {
                "title": "Select the type of electrical measurement",
                "options": {
                    MeasurementMenuOptions.NO_MEASUREMENT.value: "No electrical measurement",
                    MeasurementMenuOptions.MANUAL_VI.value: "Manual I-V range measurement",
                    MeasurementMenuOptions.MANUAL_IV.value: "Manual V-I range measurement",
                    MeasurementMenuOptions.AUTOMATIC_VI.value:"Automatic I-V range measurement",
                    MeasurementMenuOptions.AUTOMATIC_IV.value: "Automatic V-I range measurement",
                    MeasurementMenuOptions.AUTOMATIC_VT.value: "Automatic t-V range measurement",
                    MeasurementMenuOptions.AUTOMATIC_IT.value: "Automatic t-I range measurement",
                }
            },
            "current_scale": {
                "title": "Select the scale of the current measurement",
                "options": {
                    CurrentScaleOptions.MILIAMPS.value: "mA",
                    CurrentScaleOptions.MICROAMPS.value: "uA",
                    CurrentScaleOptions.NANOAMPS.value: "nA",
                }
            },
            "voltage_scale": {
                "title": "Select the scale of the voltage measurement",
                "options": {
                    VoltageScaleOptions.VOLTS.value: "V",
                    VoltageScaleOptions.MILIVOLTS.value: "mV",
                    VoltageScaleOptions.MICROVOLTS.value: "uV",
                }
            }
        }

    def display_menu(self, menu_type):
        os.system("cls" if os.name == "nt" else "clear")
        menu = self.menus.get(menu_type)
        if not menu:
            print("Invalid menu type")
            return None

        title = menu["title"]
        options = menu["options"]

        # Calculate the width of the menu
        menu_width = max(len(title), max(len(f"{key}. {desc}") for key, desc in options.items())) + 4

        print("-" + "-" * (menu_width + 2) + "-")
        # Print the title
        print(f"{title.center(menu_width)}")
        # Print a separator
        print("-" + "-" * (menu_width + 2) + "-")

        # Print the options
        for key, description in options.items():
            print(f" {key}. {description}")

        print("")

    def get_option(self, menu_type):
        menu = self.menus.get(menu_type)

        try:
            if menu_type != "mfcs":
                choice = int(input("Choose an option: "))
                while choice not in menu["options"].keys():
                    print("Invalid choice")
                    choice = int(input("Choose an option: "))
            else:
                # Handle multiple selections for MFCs
                choices = input("Choose MFCs (comma-separated): ").split(",")
                choices = list(map(int, choices))

                if not all(choice in menu["options"].keys() for choice in choices):
                    print("Invalid choice(s)")
                    return self.get_option(menu_type)
                return choices

        except ValueError:
            print("Invalid input")
            return self.get_option(menu_type)

        return choice
        
    def clear_terminal(self):
        input("Terminal will be cleared. \npress any key to continue...")
        os.system("cls" if os.name == "nt" else "clear")

    def get_user_input(self, message, min_value=float('-inf'), max_value=float('inf'), type='int'):
        try:
            if type == 'int':
                value = int(input(message))
            elif type == 'float':
                value = float(input(message))

            if value < min_value or value > max_value:
                raise ValueError()
            
            return value
        
        except ValueError:
            print(f"Input must be a number between {min_value} and {max_value}")
            return self.get_user_input(message, min_value, max_value)

        except Exception:
            print(f"Invalid input. The input must be an {type}.")
            return self.get_user_input(message, min_value, max_value)
