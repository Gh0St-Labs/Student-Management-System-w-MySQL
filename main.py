from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication \
    , QBoxLayout, QLabel, QWidget, QGridLayout \
    , QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox

from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
import mysql.connector


class DatabaseConnection():
    def __init__(self, host='localhost', user='root', password='pythonMYSQL',database='university'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user,
                                             password=self.password,
                                             database=self.database)
        return connection

class TheMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')

        # The Menus
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')
        edit_menu = self.menuBar().addMenu('&Search')

        # File Menu
        add_student_action = QAction(QIcon('199-1998497_male-user-add-icon-add-user-icon-png.png'),
                                     'Add Student', self)
        file_menu.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert)

        # Help Menu
        help_action = QAction('About', self)
        help_menu.addAction(help_action)
        help_action.triggered.connect(self.about)

        # Search Menu
        self.edit_action = QAction(QIcon('4703.png_860.png'), 'Search Student', self)
        edit_menu.addAction(self.edit_action)
        self.edit_action.triggered.connect(self.search_dialog)

        # Creating the Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)

        # Creating the Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(self.edit_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.table.cellClicked.connect(self.cell_clicked)

        self.setCentralWidget(self.table)

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):

        # Establishing SQL Queries
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students')
        result = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            print('First Loop Start')
            print(f'Row Number - {row_number}, Row Data - {row_data}')
            self.table.insertRow(row_number)  # Argument is No: of Rows. In our case, it's the index number of
            # enumerated numbers.
            for column_number, column_data in enumerate(row_data):
                print('Second Loop Start')
                print(
                    f'Row Number - {row_number}, Column Number - {column_number}, Column Data (Row-Data) - {column_data}')
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        connection.close()

    def insert(self):
        dialog = StudentDialog()
        dialog.exec()

    def search_dialog(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def edit(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        content = """
        Welcome to the Student Management System by Shuttle. 
        Feel free to add, modify and delete data!

        Read the Release Notes of the Latest Upcoming Version Below:
        https://syonisalwaysbetterthanakashatbasketball.com/confidentialreleasenotes/
        """
        self.setText(content)
        self.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = sms.table.currentRow()

        # Get Student ID
        self.student_id = sms.table.item(index, 0).text()

        # Get Student Name
        student = sms.table.item(index, 1).text()

        # Get Course
        index_course = sms.table.item(index, 2).text()

        # Get Mobile
        index_mobile = sms.table.item(index, 3).text()

        # Student Name
        self.student_name = QLineEdit(student)
        self.student_name.setPlaceholderText('Name')

        # Course Dropdown List
        self.course_box = QComboBox()
        courses = ['Physics', 'Maths', 'Biology', 'English', 'Chemistry', 'Astronomy', 'Computer Science']
        self.course_box.addItems(courses)
        self.course_box.setCurrentText(index_course)

        # Student Mobile
        self.phone = QLineEdit(index_mobile)
        self.phone.setPlaceholderText('Phone')

        # Register Button
        register_button_edit = QPushButton('Edit')
        register_button_edit.clicked.connect(self.update_student)

        layout.addWidget(self.student_name)
        layout.addWidget(self.course_box)
        layout.addWidget(self.phone)
        layout.addWidget(register_button_edit)

        self.setLayout(layout)

    def update_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s',
                       (self.student_name.text(), self.course_box.itemText(self.course_box.currentIndex()),
                        self.phone.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        sms.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Student Data')

        layout = QGridLayout()

        confirmation = QLabel('Are you sure you want to delete this record?')
        yes = QPushButton('Yes')
        yes.clicked.connect(self.delete_student)
        no = QPushButton('No')

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

    def delete_student(self):
        # Get Index and Student ID
        the_index = sms.table.currentRow()
        id = sms.table.item(the_index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('DELETE from students WHERE id=%s', (id,))
        connection.commit()
        cursor.close()
        connection.close()

        sms.load_data()

        # Close the Confirmation Window and send a popup
        self.close()
        confirmed = QMessageBox()
        confirmed.setWindowTitle('Success!')
        confirmed.setText('The Record was deleted successfully!')
        confirmed.exec()


class StudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student Name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')

        # Course Dropdown List
        self.course_box = QComboBox()
        courses = ['Physics', 'Maths', 'Biology', 'English', 'Chemistry', 'Astronomy', 'Computer Science']
        self.course_box.addItems(courses)

        # Student Mobile
        self.phone = QLineEdit()
        self.phone.setPlaceholderText('Phone')

        # Register Button
        register_button = QPushButton('Register')
        register_button.clicked.connect(self.add_student)

        layout.addWidget(self.student_name)
        layout.addWidget(self.course_box)
        layout.addWidget(self.phone)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def add_student(self):
        # Adding Student into SQL Table
        name = self.student_name.text()
        course = self.course_box.itemText(self.course_box.currentIndex())
        mobile = self.phone.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)', (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        sms.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        edit_layout = QVBoxLayout()

        # Name to find and button to function
        self.search = QLineEdit()
        self.search.setPlaceholderText
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_dialog)

        edit_layout.addWidget(self.search)
        edit_layout.addWidget(search_button)

        self.setLayout(edit_layout)

    def search_dialog(self):
        # Implementing the Search Function
        name = self.search.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students WHERE name = %s', (name,))
        result = cursor.fetchall()
        row_result = list(result)

        items = sms.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for a_item in items:
            sms.table.item(a_item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


setup_app = QApplication(sys.argv)
sms = TheMainWindow()
sms.show()
sms.load_data()
sys.exit(setup_app.exec())