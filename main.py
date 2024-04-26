from PySide6 import QtCore
from PySide6.QtCore import QEvent, QFileInfo
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from random import randint
from ui.game import Ui_MainWindow as GameUi
from ui.menu import Ui_MainWindow as MenuUi
from res.stone import Stone


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_ui = MenuUi()
        self.game_ui = GameUi()
        self.menu_ui.setupUi(self)
        self.st_list = []

        self.take_last_win = False
        self.pl_vs_pl = False
        self.turn = False

        self.menu_ui.pushButton.clicked.connect(self.menu_handler)
        self.menu_ui.pushButton_2.clicked.connect(self.load_game)

    def menu_handler(self):

        print(self.menu_ui.comboBox.currentIndex())
        if self.menu_ui.comboBox.currentIndex() == 0:
            self.take_last_win = True
            print('take_last_win')
        else:
            self.take_last_win = False

        self.pl_vs_pl = False

        if self.menu_ui.comboBox_2.currentIndex() == 1:
            print("pl_vs_pl")
            self.pl_vs_pl = True
        # print(self.take_last_win)
        self.game_ui.setupUi(self)
        self.game_ui.label.setText("1 Player")
        self.game_ui.pushButton.clicked.connect(self.save_game)
        for i in range(randint(10, 101)):
            self.st_list.append(Stone())
            self.st_list[i].installEventFilter(self)
            self.st_list[i].clicked.connect(self.remove)
            self.game_ui.verticalLayout.addWidget(self.st_list[i])

    def load_game(self):
        dlg = QFileDialog()
        dlg.setNameFilter("*.save")
        dlg.setFileMode(QFileDialog.ExistingFile)
        if dlg.exec():
            with open(QFileInfo(dlg.selectedFiles()[0]).path() + '/' + QFileInfo(dlg.selectedFiles()[0]).fileName()) as file:
                data = file.read().split()
                self.pl_vs_pl = bool(int(data[0]))
                self.take_last_win = bool(int(data[1]))
                ncount = int(data[2])
                self.turn = bool(int(data[3]))
            self.game_ui.setupUi(self)
            self.game_ui.label.setText(f"{int(self.turn) + 1} Player")
            self.game_ui.pushButton.clicked.connect(self.save_game)
            for i in range(ncount):
                self.st_list.append(Stone())
                self.st_list[i].installEventFilter(self)
                self.st_list[i].clicked.connect(self.remove)
                self.game_ui.verticalLayout.addWidget(self.st_list[i])


    def save_game(self):
        with open(f"saves/{self.game_ui.lineEdit.text()}.save", 'w') as save:
            save.write(f"{int(self.pl_vs_pl)}\n{int(self.take_last_win)}\n{len(self.st_list)}"
                       f"\n{int(self.turn)}")

    def remove(self):
        mx = 0
        for elem in self.st_list:
            if elem.hov == True:
                mx += 1
            if mx > 4:
                return
        for i in range(mx):
            self.st_list[0].hide()
            self.st_list = self.st_list[1:]
        if self.pl_vs_pl:
            self.pl_game()
        else:
            self.copm_game()

    def qremove(self, num, nc=True):
        num = min(len(self.st_list), num)
        for i in range(num):
            self.st_list[0].hide()
            self.st_list = self.st_list[1:]
        if self.pl_vs_pl:
            print(11)
            self.pl_game()
        else:
            if nc:
                self.copm_game()

    def copm_game(self):
        if self.st_list == []:
            if self.take_last_win:
                self.game_ui.label.setText(f"{int(self.turn) + 1} Player Win")
                return
            else:
                self.game_ui.label.setText(f"{int(not self.turn) + 1} Player Win")
                return
        if True:
            print('cp_turn')
            if len(self.st_list) > 8:
                self.qremove(4, nc=False)
                print(4)
            elif 4 < len(self.st_list) <= 8:
                if True:
                    self.qremove(max(1, len(self.st_list) - 5), nc=False)
                    print(max(1, len(self.st_list) - 5))
            elif 0 < len(self.st_list) <= 4:
                if self.take_last_win:
                    self.qremove(max(1, len(self.st_list)), nc=False)
                    print(max(1, len(self.st_list)))

                else:
                    self.qremove(max(1, len(self.st_list) - 1), nc=False)
                    print(max(1, len(self.st_list) - 1))

        # self.turn = not self.turn

    def pl_game(self):
        if self.st_list == []:
            if self.take_last_win:
                self.game_ui.label.setText(f"{int(self.turn) + 1} Player Win")
                return
            else:
                self.game_ui.label.setText(f"{int(not self.turn) + 1} Player Win")
                return
        self.turn = not self.turn
        self.game_ui.label.setText(f"{int(self.turn) + 1} Player")

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.Enter:
            for i in range(self.st_list.index(obj) + 1):
                self.st_list[i].ghover()
        if ev.type() == QEvent.Leave:
            for elem in self.st_list:
                elem.not_ghover()
        if ev.type() == QEvent.KeyPress:
            pass

        return False

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_1:
            self.qremove(1)
        elif key == QtCore.Qt.Key_2:
            self.qremove(2)
        elif key == QtCore.Qt.Key_3:
            self.qremove(3)
        elif key == QtCore.Qt.Key_4:
            self.qremove(4)

        else:
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
