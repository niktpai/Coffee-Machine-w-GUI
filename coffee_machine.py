"""
Assignment #1
CS 7375
Nikhil Pai

Implementing a model-based AI agent
Coffee Maker

"""
# Imports for data class
from dataclasses import dataclass
# Imports for behavioral class
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QColor


@dataclass
class CoffeeVariables:
    """This data class is responsible for containing data relevant to the coffee brewing decision making.

    Instance Variables:
        water: this boolean represents whether the correct amount of water has been added to the machine's tank
        coffee_grounds_loaded: this boolean represents whether new coffee grounds have been added to the machine's filter basket
        carafe_empty: this boolean represents whether the carafe has been removed and emptied.

    Returns:
        _type_: CoffeeVariables()
    """
    water: bool = False  # default value
    coffee_grounds_loaded: bool = False
    carafe_empty: bool = True

    def set_water(self, value: bool) -> None:
        """ Sets self.water to arg value typecast to a boolean

        Args:
            value (bool): argument to set self.water
        """
        self.water = bool(value)

    def set_coffee_grounds(self, value: bool) -> None:
        """Sets self.coffee_grounds_loaded to arg value typecast to a boolean

        Args:
            value (bool): argument to set self.coffee_grounds_loaded
        """
        self.coffee_grounds_loaded = bool(value)

    def set_carafe_empty(self, value: bool) -> None:
        """Sets self.carafe_empty to arg value typecast to a boolean

        Args:
            value (bool): argument to set self.carafe_empty
        """
        self.carafe_empty = bool(value)

    def is_ready(self) -> bool:
        """Checks if all the conditions are meet to brew

        Returns:
            bool: whether all conditions are meet
        """
        if self.water and self.coffee_grounds_loaded and self.carafe_empty:
            return True

        return False


class CoffeeMaker(QWidget):
    """
    This is the behavioral class that is responsible for all the functionality and decision making.

    Args:
        QWidget (_type_): Main Window Widget
    """

    def __init__(self):
        """ Initialization Function
        """
        super().__init__()
        # initializing and declaring object to store coffee variables
        self.coffee_variables = CoffeeVariables()
        # initializing and declaring variable to store the 3 possible states
        self.states = ["IDLE", "BREWING", "FINISHED"]
        # function to create UI
        self.initUI()

    def initUI(self):
        """This function creates the layout and all necessary widgets for the UI
        """
        self.setWindowTitle('Coffee Maker')

        layout = QVBoxLayout()

        # State Label
        self.state = self.states[0]
        self.state_label = QLabel(f'State: {self.state}')
        layout.addWidget(self.state_label)

        # Coffee Type ComboBox
        self.coffee_label = QLabel('Select Coffee Amount:')
        layout.addWidget(self.coffee_label)
        self.coffee_combo = QComboBox()
        self.coffee_combo.addItem('4oz')
        self.coffee_combo.addItem('8oz')
        self.coffee_combo.addItem('12oz')
        self.coffee_combo.currentIndexChanged.connect(
            lambda: self.update_status_bar(f'Selected: {self.coffee_combo.currentText()}'))
        layout.addWidget(self.coffee_combo)

        # LEDs for boolean variables
        led_layout = QHBoxLayout()

        self.water_led = QLabel()
        self.water_led.setFixedWidth(100)
        self.set_led_color(self.water_led, False)  # Initially set to red
        led_layout.addWidget(self.water_led)

        self.coffee_grounds_led = QLabel()
        self.coffee_grounds_led.setFixedWidth(100)
        self.set_led_color(self.coffee_grounds_led,
                           False)  # Initially set to red
        led_layout.addWidget(self.coffee_grounds_led)

        self.empty_carafe_led = QLabel()
        self.empty_carafe_led.setFixedWidth(100)
        # Initially set to green
        self.set_led_color(self.empty_carafe_led, True)
        led_layout.addWidget(self.empty_carafe_led)

        layout.addLayout(led_layout)

        # Labels for LEDS
        led_label_layout = QHBoxLayout()

        self.water_label = QLabel()
        self.water_label.setFixedWidth(100)
        self.water_label.setText("Water Level")
        led_label_layout.addWidget(self.water_label)

        self.coffee_label = QLabel()
        self.coffee_label.setFixedWidth(100)
        self.coffee_label.setText("Coffee Grounds")
        led_label_layout.addWidget(self.coffee_label)

        self.carafe_label = QLabel()
        self.carafe_label.setFixedWidth(100)
        self.carafe_label.setText("Carafe Empty")
        led_label_layout.addWidget(self.carafe_label)

        layout.addLayout(led_label_layout)

        # Buttons for Conditions
        condition_button_layout = QHBoxLayout()

        self.water_level_button = QPushButton("Add Water")
        self.water_level_button.clicked.connect(self.water_button_action)
        self.water_level_button.clicked.connect(self.check_for_reset)
        condition_button_layout.addWidget(self.water_level_button)

        self.coffee_grounds_button = QPushButton("Add Coffee Grounds")
        self.coffee_grounds_button.clicked.connect(
            self.coffee_grounds_button_action)
        self.coffee_grounds_button.clicked.connect(self.check_for_reset)
        condition_button_layout.addWidget(self.coffee_grounds_button)

        self.empty_carafe_button = QPushButton("Empty Carafe")
        self.empty_carafe_button.clicked.connect(
            self.empty_carafe_button_action)
        self.empty_carafe_button.clicked.connect(self.check_for_reset)
        condition_button_layout.addWidget(self.empty_carafe_button)

        layout.addLayout(condition_button_layout)

        # Brew Button
        self.brew_button = QPushButton('Brew Coffee')
        self.brew_button.clicked.connect(self.start_brewing)
        layout.addWidget(self.brew_button)

        # Status Bar
        self.status_bar = QStatusBar()
        layout.addWidget(self.status_bar)
        self.update_status_bar("Idle")

        self.setLayout(layout)
        self.show()

    def update_status_bar(self, message: str):
        """This will update the status bar with given message

        Args:
            message (String): the message to be displayed
        """
        self.status_bar.showMessage(message)

    def set_led_color(self, led: QLabel, state: bool):
        """Function will set led to desired color

        Args:
            led (QLabel): _description_
            state (bool): _description_
        """
        color = QColor('green') if state else QColor('red')
        led.setStyleSheet(f'background-color: {color.name()}')

    def update_state_and_label(self, state: str):
        """Function will update the machine's state and the state label

        Args:
            state (str): new state of coffee machine
        """
        self.state = state
        self.state_label.setText(f'State: {self.state}')

    def water_button_action(self):
        """updates the water variable and the status bar of this recent action
        """
        self.update_water(True)
        self.update_status_bar(f'Added Water')

    def coffee_grounds_button_action(self):
        """updates the coffee grounds variable and the status bar of this recent action
        """
        self.update_coffee_grounds(True)
        self.update_status_bar(f'Added Coffee Grounds')

    def empty_carafe_button_action(self):
        """updates the carafe variable and the status bar of this recent action
        """
        self.update_empty_carafe(True)
        self.update_status_bar(f'Emptied Carafe')

    def check_for_reset(self):
        """Function will check if the conditions are meet to change the state to Idle
        """
        if self.coffee_variables.is_ready():
            if not self.state == self.states[0]:
                # Sets state as 'Idle'
                self.update_state_and_label(self.states[0])
                self.update_status_bar(f'Reset to Idle')

    def update_water(self, Value: bool):
        """Sets the water variable to desired value and updates the led to match

        Args:
            Value (bool): desired value
        """
        self.coffee_variables.set_water(Value)
        self.set_led_color(self.water_led, Value)

    def update_coffee_grounds(self, Value: bool):
        """Sets the coffee grounds variable to desired value and updates the led to match

        Args:
            Value (bool): desired value
        """
        self.coffee_variables.set_coffee_grounds(Value)
        self.set_led_color(self.coffee_grounds_led, Value)

    def update_empty_carafe(self, Value: bool):
        """Sets the carafe variable to desired value  and updates the led to match

        Args:
            Value (bool): desired value
        """
        self.coffee_variables.set_carafe_empty(Value)
        self.set_led_color(self.empty_carafe_led, Value)

    def start_brewing(self):
        """This function will intiate the brewing process. If the brew fails the user will be notified.
        """
        if self.state == self.states[0] and self.coffee_variables.is_ready():
            # Sets state as 'Brewing'
            self.update_state_and_label(self.states[1])
            selected_coffee = self.coffee_combo.currentText()
            self.update_status_bar(f'Brewing {selected_coffee}...')
            self.start_brew_timer()
        else:
            self.update_status_bar("Conditions Not Meet")

    def start_brew_timer(self):
        """Function simulates the wait time for the brewing process.
        """
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)  # Run the timer only once
        self.timer.timeout.connect(self.brew_finished)
        self.timer.start(2000)  # Wait for 2 seconds (2000 milliseconds)

    def brew_finished(self):
        """Function updates the machine after brewing is finished
        """
        self.update_state_and_label('FINISHED')
        self.update_water(False)
        self.update_coffee_grounds(False)
        self.update_empty_carafe(False)
        selected_coffee = self.coffee_combo.currentText()
        self.update_status_bar(f'Finished Brewing {selected_coffee}')


if __name__ == '__main__':
    # Create and launch the app
    app = QApplication(sys.argv)
    coffee_maker_gui = CoffeeMaker()
    sys.exit(app.exec_())