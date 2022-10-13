import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QFileDialog, QLabel, QScrollArea, QWidget, \
    QTableWidgetItem, QPushButton, QInputDialog
import sys

con = sqlite3.connect("test.db")


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('1.ui', self)

        self.lineEdit.textChanged[str].connect(self.new_text)
        self.pushButton.clicked.connect(self.search_courses)

        self.position = ''
        self.lst_courses = []

        self.updata_tw()

    def new_text(self, text):
        self.position = text
        print(self.position)

    def search_courses(self):
        # алгоритм поиска self.position
        self.update()

    def update(self):
        self.result = [('', '')]
        # парс таблици
        self.result = self.result
        self.updata_tw()

    def updata_tw(self):
        self.con = sqlite3.connect("Сourses.db")
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM competencies").fetchall()
        print(result)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        # для ex
        '''
                self.result = [('', '')]
        # парс таблици
        self.result = self.result

        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        '''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())