from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QFileDialog, QLabel, QScrollArea, QWidget, \
    QTableWidgetItem, QPushButton, QInputDialog
import sys
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Диалоговые окна')

        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("Кнопка")
        self.button_1.clicked.connect(self.run)

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Введите имя фыйла",
                                                "Введите название фыйла")
        if ok_pressed:
            f1 = open(f"{name}.txt", 'w', encoding='utf-8')
            con = sqlite3.connect('my_base.sqlite')
            cur = con.cursor()
            result = cur.execute("""SELECT * FROM rings""").fetchall()
            for num, elem in enumerate(result):
                print(f'Урок № {num + 1} c {elem[0]} до {elem[1]}', file=f1)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('1.ui', self)

        self.pixmap = QPixmap("B.jpg")
        self.back.setPixmap(self.pixmap)

        self.pushButton.clicked.connect(self.write_text_file)
        self.pushButton_2.clicked.connect(self.style_button)
        self.pushButton_3.clicked.connect(self.background)
        self.pushButton_4.clicked.connect(self.style_text)

        w = QWidget()
        w.setLayout(self.verticalLayout)
        self.scrollArea.setWidget(w)

        self.con = sqlite3.connect("my_base.sqlite")
        cur = self.con.cursor()
        self.con_2 = sqlite3.connect("lessons.sqlite")
        cur_2 = self.con_2.cursor()

        self.modified = {}
        self.titles = None
        self.row = 0
        self.update_rings()

        self.modified_mo = {}
        self.titles_mo = None
        self.row_mo = 0
        self.update_mo()

        self.modified_tu = {}
        self.titles_tu = None
        self.row_tu = 0
        self.update_tu()

        self.modified_we = {}
        self.titles_we = None
        self.row_we = 0
        self.update_we()

        self.modified_th = {}
        self.titles_th = None
        self.row_th = 0
        self.update_th()

        self.modified_fr = {}
        self.titles_fr = None
        self.row_fr = 0
        self.update_fr()

        self.tableWidget.itemChanged.connect(self.item_changed_rings)
        self.spinBox.valueChanged.connect(self.row_rind)

        self.tableWidget_mo.itemChanged.connect(self.item_changed_mo)
        self.spinBox_mo.valueChanged.connect(self.row_monday)

        self.tableWidget_tu.itemChanged.connect(self.item_changed_tu)
        self.spinBox_tu.valueChanged.connect(self.row_tuesday)

        self.tableWidget_we.itemChanged.connect(self.item_changed_we)
        self.spinBox_we.valueChanged.connect(self.row_wednesday)

        self.tableWidget_th.itemChanged.connect(self.item_changed_th)
        self.spinBox_th.valueChanged.connect(self.row_thursday)

        self.tableWidget_fr.itemChanged.connect(self.item_changed_fr)
        self.spinBox_fr.valueChanged.connect(self.row_friday)

        self.spinBox.setMinimum(1)
        result = cur.execute("""SELECT COUNT(*) FROM rings""").fetchall()
        self.spinBox.setValue(*result[0])
        self.num = result[0][0]

        self.spinBox_mo.setMinimum(1)
        result = cur_2.execute("""SELECT COUNT(*) FROM Monday""").fetchall()
        self.spinBox_mo.setValue(*result[0])
        self.num_mo = result[0][0]

        self.spinBox_tu.setMinimum(1)
        result = cur_2.execute("""SELECT COUNT(*) FROM Tuesday""").fetchall()
        self.spinBox_tu.setValue(*result[0])
        self.num_tu = result[0][0]

        self.spinBox_we.setMinimum(1)
        result = cur_2.execute("""SELECT COUNT(*) FROM Wednesday""").fetchall()
        self.spinBox_we.setValue(*result[0])
        self.num_we = result[0][0]

        self.spinBox_th.setMinimum(1)
        result = cur_2.execute("""SELECT COUNT(*) FROM Thursday""").fetchall()
        self.spinBox_th.setValue(*result[0])
        self.num_th = result[0][0]

        self.spinBox_fr.setMinimum(1)
        result = cur_2.execute("""SELECT COUNT(*) FROM Friday""").fetchall()
        self.spinBox_fr.setValue(*result[0])
        self.num_fr = result[0][0]

    def write_text_file(self):
        ex_2 = Example()
        ex_2.run()

    def style_button(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pushButton_2.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_3.setStyleSheet("background-color: {}".format(color.name()))
            self.pushButton_4.setStyleSheet("background-color: {}".format(color.name()))

    def style_text(self):
        color = QColorDialog.getColor()
        try:
            if color.isValid():
                col = (color.getRgb()[0], color.getRgb()[1], color.getRgb()[2])
                col = '#%02x%02x%02x' % col
                self.label_2.setText(f'<font color="{col}">{(self.label_2.text())}</font>')
                self.label_3.setText(f'<div style="color: rgb{color.getRgb()};">{self.label_3.text()}</div>')
                self.label_4.setText(f'<div style="color: rgb{color.getRgb()};">{self.label_4.text()}</div>')
                self.label_5.setText(f'<div style="color: rgb{color.getRgb()};">{self.label_5.text()}</div>')
                self.label_6.setText(f'<div style="color: rgb{color.getRgb()};">{self.label_6.text()}</div>')
                self.label_7.setText(f'<div style="color: rgb{color.getRgb()};">{self.label_7.text()}</div>')
        except Exception as e:
            print(e)

    def background(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
            self.pixmap = QPixmap(fname)
            self.back.setPixmap(self.pixmap)
        except Exception:
            pass

    def update_rings(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM rings",
                             ).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed_rings(self, item):
        self.modified[self.titles[item.column()]] = item.text()
        self.row = item.row()
        self.save_rings()

    def save_rings(self):
        try:
            cur = self.con.cursor()
            que = "UPDATE rings SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += " WHERE ROWID = ?"
            cur.execute(que, (str(self.row + 1),))
            self.con.commit()
            self.modified.clear()
        except Exception as e:
            print(e)

    def row_rind(self):
        new_num = self.spinBox.value()
        cur = self.con.cursor()
        try:
            if new_num < self.num:
                result = cur.execute("""DELETE from rings WHERE ROWID > ?""", str(new_num)).fetchall()
            else:
                for i in range(new_num - self.num):
                    result = cur.execute("""INSERT INTO rings VALUES (NULL, NULL)""").fetchall()
            self.con.commit()
            self.update_rings()
            self.num = new_num
        except Exception as e:
            pass

    def update_mo(self):
        cur_2 = self.con_2.cursor()
        result = cur_2.execute("SELECT * FROM Monday",
                               ).fetchall()
        self.tableWidget_mo.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget_mo.setColumnCount(len(result[0]))
        self.titles_mo = [description[0] for description in cur_2.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_mo.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified_mo = {}

    def item_changed_mo(self, item):
        self.modified_mo[self.titles_mo[item.column()]] = item.text()
        self.row_mo = item.row()
        self.save_mo()

    def save_mo(self):
        try:
            cur_2 = self.con_2.cursor()
            que = "UPDATE Monday SET\n"
            que += ", ".join([f"{key}='{self.modified_mo.get(key)}'"
                              for key in self.modified_mo.keys()])
            que += " WHERE ROWID = ?"
            cur_2.execute(que, (str(self.row_mo + 1),))
            self.con_2.commit()
            self.modified_mo.clear()
        except Exception as e:
            print(e)

    def row_monday(self):
        new_num_mo = self.spinBox_mo.value()
        cur_2 = self.con_2.cursor()
        try:
            if new_num_mo < self.num_mo:
                result = cur_2.execute("""DELETE from Monday WHERE ROWID > ?""", str(new_num_mo)).fetchall()
            else:
                for i in range(new_num_mo - self.num_mo):
                    result = cur_2.execute("""INSERT INTO Monday VALUES (NULL)""").fetchall()
            self.con_2.commit()
            self.update_mo()
            self.num_mo = new_num_mo
        except Exception as e:
            pass

    def update_tu(self):
        cur_2 = self.con_2.cursor()
        result = cur_2.execute("SELECT * FROM Tuesday",
                               ).fetchall()
        self.tableWidget_tu.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget_tu.setColumnCount(len(result[0]))
        self.titles_tu = [description[0] for description in cur_2.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_tu.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified_tu = {}

    def item_changed_tu(self, item):
        self.modified_tu[self.titles_tu[item.column()]] = item.text()
        self.row_tu = item.row()
        self.save_tu()

    def save_tu(self):
        try:
            cur_2 = self.con_2.cursor()
            que = "UPDATE Tuesday SET\n"
            que += ", ".join([f"{key}='{self.modified_tu.get(key)}'"
                              for key in self.modified_tu.keys()])
            que += " WHERE ROWID = ?"
            cur_2.execute(que, (str(self.row_tu + 1),))
            self.con_2.commit()
            self.modified_tu.clear()
        except Exception as e:
            print(e)

    def row_tuesday(self):
        new_num = self.spinBox_tu.value()
        cur_2 = self.con_2.cursor()
        try:
            if new_num < self.num_tu:
                result = cur_2.execute("""DELETE from Tuesday WHERE ROWID > ?""", str(new_num)).fetchall()
            else:
                for i in range(new_num - self.num_tu):
                    result = cur_2.execute("""INSERT INTO Tuesday VALUES (NULL)""").fetchall()
            self.con_2.commit()
            self.update_tu()
            self.num_tu = new_num
        except Exception as e:
            pass

    def update_we(self):
        cur_2 = self.con_2.cursor()
        result = cur_2.execute("SELECT * FROM Wednesday",
                               ).fetchall()
        self.tableWidget_we.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget_we.setColumnCount(len(result[0]))
        self.titles_we = [description[0] for description in cur_2.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_we.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified_we = {}

    def item_changed_we(self, item):
        self.modified_we[self.titles_we[item.column()]] = item.text()
        self.row_we = item.row()
        self.save_we()

    def save_we(self):
        try:
            cur_2 = self.con_2.cursor()
            que = "UPDATE Wednesday SET\n"
            que += ", ".join([f"{key}='{self.modified_we.get(key)}'"
                              for key in self.modified_we.keys()])
            que += " WHERE ROWID = ?"
            cur_2.execute(que, (str(self.row_we + 1),))
            self.con_2.commit()
            self.modified_we.clear()
        except Exception as e:
            print(e)

    def row_wednesday(self):
        new_num = self.spinBox_we.value()
        cur_2 = self.con_2.cursor()
        try:
            if new_num < self.num_we:
                result = cur_2.execute("""DELETE from Wednesday WHERE ROWID > ?""", str(new_num)).fetchall()
            else:
                for i in range(new_num - self.num_we):
                    result = cur_2.execute("""INSERT INTO Wednesday VALUES (NULL)""").fetchall()
            self.con_2.commit()
            self.update_we()
            self.num_we = new_num
        except Exception as e:
            pass

    def update_th(self):
        cur_2 = self.con_2.cursor()
        result = cur_2.execute("SELECT * FROM Thursday",
                               ).fetchall()
        self.tableWidget_th.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget_th.setColumnCount(len(result[0]))
        self.titles_th = [description[0] for description in cur_2.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_th.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified_th = {}

    def item_changed_th(self, item):
        self.modified_th[self.titles_th[item.column()]] = item.text()
        self.row_th = item.row()
        self.save_th()

    def save_th(self):
        try:
            cur_2 = self.con_2.cursor()
            que = "UPDATE Thursday SET\n"
            que += ", ".join([f"{key}='{self.modified_th.get(key)}'"
                              for key in self.modified_th.keys()])
            que += " WHERE ROWID = ?"
            cur_2.execute(que, (str(self.row_th + 1),))
            self.con_2.commit()
            self.modified_th.clear()
        except Exception as e:
            print(e)

    def row_thursday(self):
        new_num = self.spinBox_th.value()
        cur_2 = self.con_2.cursor()
        try:
            if new_num < self.num_th:
                result = cur_2.execute("""DELETE from Thursday WHERE ROWID > ?""", str(new_num)).fetchall()
            else:
                for i in range(new_num - self.num_th):
                    result = cur_2.execute("""INSERT INTO Thursday VALUES (NULL)""").fetchall()
            self.con_2.commit()
            self.update_th()
            self.num_th = new_num
        except Exception as e:
            pass

    def update_fr(self):
        cur_2 = self.con_2.cursor()
        result = cur_2.execute("SELECT * FROM Friday",
                               ).fetchall()
        self.tableWidget_fr.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        self.tableWidget_fr.setColumnCount(len(result[0]))
        self.titles_fr = [description[0] for description in cur_2.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_fr.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified_fr = {}

    def item_changed_fr(self, item):
        self.modified_fr[self.titles_th[item.column()]] = item.text()
        self.row_fr = item.row()
        self.save_fr()

    def save_fr(self):
        try:
            cur_2 = self.con_2.cursor()
            que = "UPDATE Friday SET\n"
            que += ", ".join([f"{key}='{self.modified_fr.get(key)}'"
                              for key in self.modified_fr.keys()])
            que += " WHERE ROWID = ?"
            cur_2.execute(que, (str(self.row_fr + 1),))
            self.con_2.commit()
            self.modified_fr.clear()
        except Exception as e:
            print(e)

    def row_friday(self):
        new_num = self.spinBox_fr.value()
        cur_2 = self.con_2.cursor()
        try:
            if new_num < self.num_fr:
                result = cur_2.execute("""DELETE from Friday WHERE ROWID > ?""", str(new_num)).fetchall()
            else:
                for i in range(new_num - self.num_fr):
                    result = cur_2.execute("""INSERT INTO Friday VALUES (NULL)""").fetchall()
            self.con_2.commit()
            self.update_fr()
            self.num_fr = new_num
        except Exception as e:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())