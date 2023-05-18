from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from threading import Thread
import sys


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(300, 325))
        self.setWindowTitle("Fraction Simplifier")
        self.setup()

    def setup(self):
        self.label_input = QLabel(parent=self, text="Input:")
        self.label_input.setGeometry(QRect(25, 5, 250, 25))
        self.label_input.setAlignment(Qt.AlignLeft)

        self.LE_input = QLineEdit(parent=self)
        self.LE_input.setText("10/20")
        self.LE_input.setGeometry(QRect(25, 25, 250, 50))
        self.LE_input.setAlignment(Qt.AlignCenter)

        self.label_output = QLabel(parent=self, text="Output:")
        self.label_output.setGeometry(QRect(25, 80, 250, 25))
        self.label_output.setAlignment(Qt.AlignLeft)

        self.LE_output = QLineEdit(parent=self)
        self.LE_output.setText("1/2")
        self.LE_output.setGeometry(QRect(25, 100, 250, 50))
        self.LE_output.setAlignment(Qt.AlignCenter)
        self.LE_output.setReadOnly(True)

        self.PB_simplify = QPushButton(parent=self, text="Simplify")
        self.PB_simplify.setGeometry(QRect(25, 175, 250, 50))
        self.PB_simplify.clicked.connect(self.start_perform)

        self.PB_exit = QPushButton(parent=self, text="Exit")
        self.PB_exit.setGeometry(QRect(25, 250, 250, 50))
        self.PB_exit.clicked.connect(self.exit)

        self.show()

    def exit(self):
        sys.exit()

    def start_perform(self):
        Thread(target=self.perform).start()

    def perform(self):
        value = self.LE_input.text()
        if "/" in value:
            if len(value.split("/")) == 2:
                numerator, denominator = value.split("/")
            else:
                self.LE_output.setText(
                    "Error: Could not split the input.")
                return 0

            if numerator.isnumeric() is True:
                numerator = int(numerator)
            else:
                self.LE_output.setText("Error: Could not convert numerator to integer.")
                return 0

            if denominator.isnumeric() is True:
                denominator = int(denominator)
            else:
                self.LE_output.setText("Error: Could not convert denominator to integer.")
                return 0

            if denominator != 0:
                factors_of_numerator = self.find_factors(numerator)
                factors_of_denominator = self.find_factors(denominator)
                self.simplify(factors_of_numerator, factors_of_denominator)
            else:
                self.LE_output.setText("Error: Division by zero.")
                return 0

        else:
            self.LE_output.setText(
                "Error: Could not split the input.")
            return 0

    @staticmethod
    def find_factors(number):
        if number == 0:
            return [0]
        elif number == 1:
            return [1]
        else:
            factors = []
            while number != 1:
                for n in range(2, number + 1):
                    if number % n == 0:
                        factors.append(n)
                        number //= n
                        break

        return factors

    @staticmethod
    def multiply(array):
        product = 1
        for number in array:
            product *= number
        return product

    def simplify(self, factors_of_numerator, factors_of_denominator):
        copy1 = factors_of_numerator[:]
        copy2 = factors_of_denominator[:]
        for element in copy1:
            if element in factors_of_denominator:
                factors_of_denominator.remove(element)
        for element in copy2:
            if element in factors_of_numerator:
                factors_of_numerator.remove(element)

        if len(factors_of_numerator) == 0:
            factors_of_numerator = [1]

        if len(factors_of_denominator) == 0:
            factors_of_denominator = [1]

        numerator = self.multiply(factors_of_numerator)
        denominator = self.multiply(factors_of_denominator)

        if denominator == 1:
            self.LE_output.setText(f"{numerator}")
        else:
            self.LE_output.setText(f"{numerator}/{denominator}")


app = QApplication(sys.argv)
gui = GUI()
app.exec_()
