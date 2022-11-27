import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import uic    # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from password import bad_pass
from bd import execute_query
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainWindow')

    def show_window_1(self):                                       # Связь окон между собой
        self.w1 = uic.loadUi('window_registration.ui', self)
        self.w1.show()
        self.w1.button_join.clicked.connect(self.click)

    def click(self):
        self.text = self.w1.input_password.text()
        print(bad_pass(self.text))
        self.name = self.w1.input_name.text()
        self.connection = sqlite3.connect('pyqt_project.db')
        self.cur = self.connection.cursor()
        result = self.cur.execute('''SELECT * FROM user WHERE name like ?''', (str(self.name),)).fetchall()
        if bad_pass(self.text) == 'ok' and len(result) == 0:
            self.w1.button_join.clicked.connect(self.show_window_2)
            create_users = f""" INSERT INTO user (name, password) VALUES ('{self.name}', '{self.text}') """
            execute_query(self.connection, create_users)
            res = self.cur.execute(f'''SELECT id FROM user WHERE name like '{self.name}' ''').fetchone()
            id = 0
            for i in res:
                id = int(i)
            create_users = f""" INSERT INTO profile (id_user, name, password) VALUES ('{id}', '{self.name}', '{self.text}') """
            execute_query(self.connection, create_users)
            self.w1.close
        elif bad_pass(self.text) == 'ok' and len(result) == 1:
            self.w1.button_join.clicked.connect(self.show_window_2)
            self.w1.close

    def show_window_2(self):
        self.w2 = uic.loadUi('window_functional.ui', self)
        self.w2.show()
        self.w2.button_profile.clicked.connect(self.show_window_3)
        self.w2.button_address.clicked.connect(self.show_window_4)
        self.w2.button_find.clicked.connect(self.show_window_5)
        self.w2.button_share.clicked.connect(self.show_window_6)
        self.w2.close

    def show_window_3(self):
        self.w3 = uic.loadUi('my_books.ui', self)
        data = self.cur.execute("SELECT * FROM my_books").fetchall()
        self.w3.tableWidget.setColumnCount(5)
        self.w3.tableWidget.setRowCount(len(data))
        self.w3.tableWidget.setHorizontalHeaderLabels(["", "ID", "Название", "Жанр", "Адрес"])
        for i, entry in enumerate(data):
            [self.w3.tableWidget.setItem(i, j, QTableWidgetItem(str(it))) for j, it in enumerate(entry)]
        self.w3.pushButton.clicked.connect(self.show_window_2)
        self.w3.close


    def show_window_4(self):
        self.w4 = uic.loadUi('maps.ui', self)
        self.pixmap = QPixmap('img.png')
        self.label_2.setPixmap(self.pixmap)
        self.w4.pushButton.clicked.connect(self.show_window_2)
        self.w4.close

    def show_window_5(self):
        self.w5 = uic.loadUi('find_book.ui', self)
        self.w5.show()
        self.w5.button_find.clicked.connect(self.click_2)
        self.w5.pushButton_2.clicked.connect(self.show_window_2)

    def click_2(self):
        self.title = self.w5.lineEdit.text()
        self.genre = self.w5.lineEdit_2.text()
        data = self.cur.execute(f'''SELECT address FROM all_books WHERE genre = '{self.genre}' and name_book = 
        '{self.title}' ''').fetchall()
        self.address = ''
        for i in data:
            for j in i:
                self.address = str(j)
        if len(data) != 0:
            self.w5.button_find.clicked.connect(self.show_window_7)
            self.w5.close
        else:
            self.w5.button_find.clicked.connect(self.show_window_8)
            self.w5.close

    def show_window_6(self):
        self.w6 = uic.loadUi('leave_book.ui', self)
        self.w6.show()
        self.count = 0
        self.w6.pushButton.clicked.connect(self.show_window_2)
        self.w6.pushButton_2.clicked.connect(self.click_4)
        self.w6.close

    def click_4(self):
        print(self.count)
        title = self.w6.lineEdit.text()
        genre = self.w6.lineEdit_2.text()
        address = self.w6.lineEdit_3.text()
        if self.count == 0:
            create_users = f""" INSERT INTO all_books (name_book, genre, address) VALUES ('{title}', '{genre}', '{address}') """
            execute_query(self.connection, create_users)
        self.w6.pushButton_2.clicked.connect(self.show_window_2)
        if self.count == 0:
            create_users = f""" INSERT INTO my_books (user_name, name_book, genre, address) VALUES ('{self.name}', '{title}', '{genre}', '{address}') """
            execute_query(self.connection, create_users)
        self.count += 1
        self.w6.close

    def show_window_7(self):
        self.w7 = uic.loadUi('book_found.ui', self)
        self.w7.lineEdit.setText(self.address)
        self.w7.show()
        self.w7.pushButton.clicked.connect(self.click_3)
        self.w7.pushButton_2.clicked.connect(self.show_window_2)
        self.w7.close

    def click_3(self):
        delete_comment = f"DELETE FROM all_books WHERE genre = '{self.genre}' and name_book = '{self.title}' and address = '{self.address}' "
        execute_query(self.connection, delete_comment)
        self.w7.pushButton.clicked.connect(self.show_window_2)
        self.w7.close

    def show_window_8(self):
        self.w8 = uic.loadUi('book_wasnt_found.ui', self)
        self.w8.show()
        self.w8.pushButton.clicked.connect(self.show_window_2)
        self.w8.pushButton_2.clicked.connect(self.show_window_9)
        self.w8.close

    def show_window_9(self):
        self.w9 = uic.loadUi('free_books.ui', self)
        self.w9.show()
        self.w9.pushButton.clicked.connect(self.show_window_2)
        self.w9.comboBox.activated[str].connect(self.onActivated)
        self.gener = 'Деловая литература'
        self.w9.pushButton_2.clicked.connect(self.search)

    def search(self):
        try:
            queue = 'SELECT * FROM all_books WHERE genre = ?'
            res = self.cur.execute(queue, (self.gener,)).fetchall()
            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(len(res[0]))
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Жанр", "Адрес"])
            for i, elem in enumerate(res):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            print(e)

    def onActivated(self, text):
        self.gener = text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.show_window_1()
    sys.exit(app.exec_())
