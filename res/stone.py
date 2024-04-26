from PySide6.QtWidgets import QLabel, QPushButton


class Stone(QPushButton):
    def __init__(self):
        super().__init__()
        self.hov = False
        self.setMouseTracking(True)
        self.setMinimumHeight(10)
        self.setStyleSheet(
            '''background-color: rgb(119, 118, 123);color: #FFFFFF;''')

    def ghover(self):
        self.hov = True
        self.setStyleSheet("background-color: rgb(40, 40, 40);color: #FFFFFF;")

    def not_ghover(self):
        self.hov = False
        self.setStyleSheet("background-color: rgb(119, 118, 123);color: #FFFFFF;")
