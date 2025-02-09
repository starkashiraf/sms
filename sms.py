import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QScrollArea, QFormLayout, QDateEdit, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import mysql.connector
from mysql.connector import Error

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1200, 800)

        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="0774976577",
                database="school_management"
            )
            self.db_cursor = self.db_connection.cursor(dictionary=True)
            self.db_connected = True
        except Error as e:
            self.db_connected = False
            print(f"Error connecting to MySQL: {e}")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.sidebar = QFrame(self.central_widget)
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar.setStyleSheet("background-color: #2C3E50;")
        self.sidebar.setFixedWidth(250)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.main_layout.addWidget(self.sidebar)

        self.content_frame = QFrame(self.central_widget)
        self.content_frame.setFrameShape(QFrame.StyledPanel)
        self.content_frame.setStyleSheet("background-color: #f0f0f0;")
        self.content_layout = QVBoxLayout(self.content_frame)
        self.main_layout.addWidget(self.content_frame)

        self.top_bar = QFrame(self.central_widget)
        self.top_bar.setFrameShape(QFrame.StyledPanel)
        self.top_bar.setStyleSheet("background-color: #34495E;")
        self.top_bar.setFixedHeight(50)
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.content_layout.addWidget(self.top_bar)

        self.account_icon = QLabel("👤")
        self.account_icon.setFont(QFont("Arial", 18))
        self.account_icon.setStyleSheet("color: white;")
        self.top_bar_layout.addWidget(self.account_icon, alignment=Qt.AlignRight)

        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.setFont(QFont("Arial", 12))
        self.dashboard_button.setStyleSheet("background-color: #2980B9; color: white;")
        self.dashboard_button.clicked.connect(self.show_dashboard)
        self.top_bar_layout.addWidget(self.dashboard_button, alignment=Qt.AlignLeft)

        self.modules = {
            "Student Management": self.show_student_management,
            "Teacher & Staff Management": self.show_teacher_management,
            "Class & Subject Management": self.show_class_management,
            "Exams & Grading": self.show_exam_grading,
            "Fees & Accounts": self.show_fees_management,
            "Library Management": self.show_library_management,
            "Hostel & Dormitory": self.show_hostel_management,
            "Transport Management": self.show_transport_management,
            "Parent & Student Portal": self.show_parent_portal,
            "Events & Calendar": self.show_events_calendar,
            "Reports & Analytics": self.show_reports_analytics
        }

        for module in self.modules.keys():
            btn = QPushButton(module)
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet("background-color: #34495E; color: white;")
            btn.clicked.connect(self.modules[module])
            self.sidebar_layout.addWidget(btn)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setFont(QFont("Arial", 12))
        self.exit_button.setStyleSheet("background-color: #C0392B; color: white;")
        self.exit_button.clicked.connect(self.close)
        self.sidebar_layout.addWidget(self.exit_button, alignment=Qt.AlignBottom)

        self.show_dashboard()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_dashboard(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Welcome to School Management System")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("background-color: #f0f0f0;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

        dashboard_frame = QFrame(self.content_frame)
        dashboard_frame.setFrameShape(QFrame.StyledPanel)
        dashboard_frame.setStyleSheet("background-color: #f0f0f0;")
        dashboard_layout = QVBoxLayout(dashboard_frame)
        self.content_layout.addWidget(dashboard_frame)

        # Cards
        cards_layout = QHBoxLayout()
        dashboard_layout.addLayout(cards_layout)

        total_students_card = self.create_card("Total Students", self.get_total_students() if self.db_connected else "N/A")
        total_teachers_card = self.create_card("Total Teachers", "50")
        cards_layout.addWidget(total_students_card)
        cards_layout.addWidget(total_teachers_card)

        # Bar Graph
        bar_graph_frame = QFrame(dashboard_frame)
        bar_graph_frame.setFrameShape(QFrame.StyledPanel)
        bar_graph_layout = QVBoxLayout(bar_graph_frame)
        dashboard_layout.addWidget(bar_graph_frame)

        bar_graph_label = QLabel("Class and Students")
        bar_graph_label.setFont(QFont("Arial", 14))
        bar_graph_layout.addWidget(bar_graph_label, alignment=Qt.AlignCenter)

        bar_graph_canvas = self.create_bar_graph()
        bar_graph_layout.addWidget(bar_graph_canvas)

        # Pie Chart
        pie_chart_frame = QFrame(dashboard_frame)
        pie_chart_frame.setFrameShape(QFrame.StyledPanel)
        pie_chart_layout = QVBoxLayout(pie_chart_frame)
        dashboard_layout.addWidget(pie_chart_frame)

        pie_chart_label = QLabel("Expenses")
        pie_chart_label.setFont(QFont("Arial", 14))
        pie_chart_layout.addWidget(pie_chart_label, alignment=Qt.AlignCenter)

        pie_chart_canvas = self.create_pie_chart()
        pie_chart_layout.addWidget(pie_chart_canvas)

    def create_card(self, title, value):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("background-color: white; border: 2px solid #ccc;")
        card_layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        card_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24))
        card_layout.addWidget(value_label, alignment=Qt.AlignCenter)

        return card

    def create_bar_graph(self):
        figure, ax = plt.subplots()
        classes = ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5']
        students = [50, 60, 70, 80, 90]
        ax.bar(classes, students, color='blue')
        ax.set_title('Number of Students in Each Class')
        ax.set_xlabel('Class')
        ax.set_ylabel('Number of Students')

        canvas = FigureCanvas(figure)
        return canvas

    def create_pie_chart(self):
        figure, ax = plt.subplots()
        labels = ['Salaries', 'Maintenance', 'Utilities', 'Miscellaneous']
        sizes = [40, 30, 20, 10]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        canvas = FigureCanvas(figure)
        return canvas

    def get_total_students(self):
        self.db_cursor.execute("SELECT COUNT(*) AS total FROM students")
        result = self.db_cursor.fetchone()
        return str(result['total'])

    def show_student_management(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Student Management")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: red;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setFont(QFont("Arial", 12))
        search_input = QLineEdit()
        search_input.setFont(QFont("Arial", 12))
        search_input.setPlaceholderText("Search by name or ID")
        search_button = QPushButton("Search")
        search_button.setFont(QFont("Arial", 12))
        search_button.setStyleSheet("background-color: #2980B9; color: white;")
        search_button.clicked.connect(lambda: self.search_student(search_input.text()))
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        self.content_layout.addLayout(search_layout)

        add_student_button = QPushButton("ADD STUDENT")
        add_student_button.setFont(QFont("Arial", 12))
        add_student_button.setStyleSheet("background-color: #2980B9; color: white;")
        add_student_button.clicked.connect(self.add_student)
        self.content_layout.addWidget(add_student_button, alignment=Qt.AlignCenter)

        self.student_list_widget = QWidget()
        self.student_list_layout = QVBoxLayout(self.student_list_widget)
        self.content_layout.addWidget(self.student_list_widget)

        self.update_student_list()

    def add_student(self, student=None):
        self.clear_layout(self.content_layout)
        label = QLabel("Add Student" if student is None else "Edit Student")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: red;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.content_layout.addWidget(scroll_area)

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        scroll_area.setWidget(form_widget)

        student_info = [
            ("First Name", QLineEdit),
            ("Last Name", QLineEdit),
            ("Date of Birth", QDateEdit),
            ("Gender", QComboBox, ["Male", "Female", "Other"]),
            ("Nationality", QComboBox, ["Select Country", "USA", "Canada", "UK", "Australia", "India", "China", "Japan", "Germany", "France", "Other"]),
            ("Place of Birth", QLineEdit),
            ("Home Address", QLineEdit),
            ("Contact Information", QLineEdit),
            ("Class", QComboBox, ["Select Class", "Class 1", "Class 2", "Class 3", "Class 4", "Class 5"]),
            ("Stream", QComboBox, ["Select Stream", "Science", "Commerce", "Arts"]),
            ("House", QComboBox, ["Select House", "Red", "Blue", "Green", "Yellow"]),
            ("Date of Joining", QDateEdit),
            ("Role", QLineEdit)
        ]

        guardian_info = [
            ("Guardian ID", QLineEdit),
            ("Parent/Guardian Name", QLineEdit),
            ("Relationship to Student", QLineEdit),
            ("Parent/Guardian Contact", QLineEdit),
            ("Occupation", QLineEdit)
        ]

        self.entries = {}
        for label_text, widget, *options in student_info:
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 12))
            if widget == QComboBox:
                entry = widget()
                entry.addItems(options[0])
            else:
                entry = widget()
            entry.setFont(QFont("Arial", 12))
            form_layout.addRow(label, entry)
            self.entries[label_text] = entry

        for label_text, widget in guardian_info:
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 12))
            entry = widget()
            entry.setFont(QFont("Arial", 12))
            form_layout.addRow(label, entry)
            self.entries[label_text] = entry

        if student:
            self.populate_student_form(student)

        save_button = QPushButton("SAVE")
        save_button.setFont(QFont("Arial", 12))
        save_button.setStyleSheet("background-color: #27AE60; color: white;")
        save_button.clicked.connect(lambda: self.save_student(student))
        self.content_layout.addWidget(save_button, alignment=Qt.AlignCenter)

    def populate_student_form(self, student):
        self.entries["First Name"].setText(student["first_name"])
        self.entries["Last Name"].setText(student["last_name"])
        self.entries["Date of Birth"].setDate(QDate.fromString(student["date_of_birth"], "yyyy-MM-dd"))
        self.entries["Gender"].setCurrentText(student["gender"])
        self.entries["Nationality"].setCurrentText(student["nationality"])
        self.entries["Place of Birth"].setText(student["place_of_birth"])
        self.entries["Home Address"].setText(student["home_address"])
        self.entries["Contact Information"].setText(student["contact_information"])
        self.entries["Class"].setCurrentText(student["class"])
        self.entries["Stream"].setCurrentText(student["stream"])
        self.entries["House"].setCurrentText(student["house"])
        self.entries["Date of Joining"].setDate(QDate.fromString(student["date_of_joining"], "yyyy-MM-dd"))
        self.entries["Role"].setText(student["role"])
        self.entries["Guardian ID"].setText(student["guardian_id"])
        self.entries["Parent/Guardian Name"].setText(student["guardian_name"])
        self.entries["Relationship to Student"].setText(student["relationship_to_student"])
        self.entries["Parent/Guardian Contact"].setText(student["guardian_contact"])
        self.entries["Occupation"].setText(student["occupation"])

    def save_student(self, student=None):
        student_data = {label: entry.text() if isinstance(entry, QLineEdit) else entry.currentText() for label, entry in self.entries.items()}
        if student:
            query = """
                UPDATE students SET first_name=%s, last_name=%s, date_of_birth=%s, gender=%s, nationality=%s, place_of_birth=%s, home_address=%s, contact_information=%s, class=%s, stream=%s, house=%s, date_of_joining=%s, role=%s, guardian_id=%s, guardian_name=%s, relationship_to_student=%s, guardian_contact=%s, occupation=%s
                WHERE id=%s
            """
            values = (
                student_data["First Name"], student_data["Last Name"], student_data["Date of Birth"], student_data["Gender"], student_data["Nationality"], student_data["Place of Birth"], student_data["Home Address"], student_data["Contact Information"], student_data["Class"], student_data["Stream"], student_data["House"], student_data["Date of Joining"], student_data["Role"], student_data["Guardian ID"], student_data["Parent/Guardian Name"], student_data["Relationship to Student"], student_data["Parent/Guardian Contact"], student_data["Occupation"], student["id"]
            )
        else:
            query = """
                INSERT INTO students (first_name, last_name, date_of_birth, gender, nationality, place_of_birth, home_address, contact_information, class, stream, house, date_of_joining, role, guardian_id, guardian_name, relationship_to_student, guardian_contact, occupation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                student_data["First Name"], student_data["Last Name"], student_data["Date of Birth"], student_data["Gender"], student_data["Nationality"], student_data["Place of Birth"], student_data["Home Address"], student_data["Contact Information"], student_data["Class"], student_data["Stream"], student_data["House"], student_data["Date of Joining"], student_data["Role"], student_data["Guardian ID"], student_data["Parent/Guardian Name"], student_data["Relationship to Student"], student_data["Parent/Guardian Contact"], student_data["Occupation"]
            )
        self.db_cursor.execute(query, values)
        self.db_connection.commit()
        self.show_student_management()

    def update_student_list(self):
        if not self.db_connected:
            return

        self.db_cursor.execute("SELECT * FROM students")
        students = self.db_cursor.fetchall()

        table = QTableWidget()
        table.setRowCount(len(students))
        table.setColumnCount(10)
        table.setHorizontalHeaderLabels(["First Name", "Last Name", "Class", "Stream", "ID", "Guardian Contact", "House", "Date of Joining", "Role", "Action"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, student in enumerate(students):
            table.setItem(row, 0, QTableWidgetItem(student["first_name"]))
            table.setItem(row, 1, QTableWidgetItem(student["last_name"]))
            table.setItem(row, 2, QTableWidgetItem(student["class"]))
            table.setItem(row, 3, QTableWidgetItem(student["stream"]))
            table.setItem(row, 4, QTableWidgetItem(student["id"]))
            table.setItem(row, 5, QTableWidgetItem(student["guardian_contact"]))
            table.setItem(row, 6, QTableWidgetItem(student["house"]))
            table.setItem(row, 7, QTableWidgetItem(student["date_of_joining"]))
            table.setItem(row, 8, QTableWidgetItem(student["role"]))

            action_button = QPushButton("Action")
            action_button.setFont(QFont("Arial", 12))
            action_button.setStyleSheet("background-color: #2980B9; color: white;")
            action_button.setMenu(self.create_action_menu(student))
            table.setCellWidget(row, 9, action_button)

        self.student_list_layout.addWidget(table)

    def create_action_menu(self, student):
        menu = QMenu()
        edit_action = menu.addAction("EDIT")
        delete_action = menu.addAction("DELETE")
        view_action = menu.addAction("VIEW")

        edit_action.triggered.connect(lambda: self.add_student(student))
        delete_action.triggered.connect(lambda: self.confirm_delete_student(student))
        view_action.triggered.connect(lambda: self.view_student(student))

        return menu

    def confirm_delete_student(self, student):
        reply = QMessageBox.question(self, 'Delete Student', f"Do you want to delete {student['first_name']} {student['last_name']}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_student(student)

    def delete_student(self, student):
        self.db_cursor.execute("DELETE FROM students WHERE id=%s", (student["id"],))
        self.db_connection.commit()
        self.update_student_list()

    def view_student(self, student):
        print(f"Viewing student: {student}")

    def search_student(self, query):
        self.db_cursor.execute("SELECT * FROM students WHERE first_name LIKE %s OR last_name LIKE %s OR id LIKE %s", (f"%{query}%", f"%{query}%", f"%{query}%"))
        students = self.db_cursor.fetchall()
        self.update_student_list(students)

    def show_teacher_management(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Teacher & Staff Management")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: blue;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_class_management(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Class & Subject Management")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: green;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_exam_grading(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Exams & Grading")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: red;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_fees_management(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Fees & Accounts")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: purple;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_library_management(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Library Management")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: brown;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_hostel_management(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Hostel & Dormitory Management")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: orange;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_transport_management(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Transport Management")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: yellow;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_parent_portal(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Parent & Student Portal")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: purple;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_events_calendar(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Events & Calendar")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: blue;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

    def show_reports_analytics(self):
        self.clear_layout(self.content_layout)
        label = QLabel("Reports & Analytics")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color: green;")
        self.content_layout.addWidget(label, alignment=Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
