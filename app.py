# Import necessary PyQt5 modules and other dependencies
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
                             QDesktopWidget, QMessageBox, QHBoxLayout, QScrollArea, QCheckBox, QButtonGroup)
from PyQt5.QtGui import QPixmap, QCursor
import sys
from functools import partial
import controller
import model
import json


# Define a class for the expanded visualization page
class ExpandVisualisationPage(QWidget):
    # Center the window in the middle of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Initialize the expanded visualization page with necessary attributes
    def __init__(self, data_visualisation_page, step_content):
        super().__init__()
        self.data_visualisation_page = data_visualisation_page
        self.login_window = login_window
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle("Visualisation Page")
        self.center()

        layout = QVBoxLayout(self)

        # Add a disconnect button
        disconnect_button = QPushButton("Disconnect", self)
        disconnect_button.setCursor(QCursor(Qt.PointingHandCursor))
        disconnect_button.setStyleSheet("color: #ffffff; background-color: #5766F9; font-size: 12pt; border-radius: "
                                        "10px;")
        disconnect_button.clicked.connect(self.disconnect)
        disconnect_button.setFixedWidth(100)
        disconnect_button.setStyleSheet("""
            QPushButton:pressed {
                background-color: #3c476c;
            }
        """)
        layout.addWidget(disconnect_button, alignment=Qt.AlignTop | Qt.AlignRight)

        controller.create_label(self, layout, 'Welcome to the expanded visualisation page',
                                "color: #5766F9; font-size: 16pt;")

        controller.create_label(self, layout, step_content,
                                "color: #ffffff; background-color: #4eafa3; font-size: 24pt; margin: 5px; "
                                "padding: 5px; border-radius: 10px;")

        # Add a return button
        return_button = QPushButton("Return", self)
        return_button.setCursor(QCursor(Qt.PointingHandCursor))
        return_button.setStyleSheet("color: #ffffff; background-color: #5766F9; font-size: 12pt; border-radius: "
                                    "10px;")
        return_button.clicked.connect(self.back)
        return_button.setFixedWidth(100)
        return_button.setStyleSheet("""
            QPushButton:pressed {
                background-color: #3c476c;
            }
        """)
        layout.addWidget(return_button, alignment=Qt.AlignBottom | Qt.AlignLeft)

    # Show a confirmation dialog before disconnecting
    def disconnect(self):
        # Show a confirmation dialog
        reply = QMessageBox.question(self, 'Disconnect', 'Are you sure you want to disconnect?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Close the authenticated page and show the login window
            self.close()
            self.login_window.show()

    def back(self):
        self.close()
        self.data_visualisation_page.show()


# Define a class for the data visualization page
class DataVisualisation(QWidget):
    # Center the window on the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle("Data Visualisation")
        self.center()
        self.labels_data = model.fetch_data_from_database()

        main_layout = QVBoxLayout(self)

        # First part of the authenticated page
        first_part = QWidget()
        first_part_layout = QVBoxLayout(first_part)

        controller.create_label(self, first_part_layout, "Welcome to the Data Visualisation",
                                "color: #5766F9; font-size: 16pt;")

        controller.create_label(self, first_part_layout, "You are now logged in.",
                                "color: #7E7E7E; font-size: 12pt;")

        # Add a disconnect button
        disconnect_button = QPushButton("Disconnect", self)
        disconnect_button.setCursor(QCursor(Qt.PointingHandCursor))
        disconnect_button.setStyleSheet("color: #ffffff; background-color: #5766F9; font-size: 12pt; border-radius: "
                                        "10px;")
        disconnect_button.clicked.connect(self.disconnect)
        disconnect_button.setFixedWidth(100)
        disconnect_button.setStyleSheet("""
            QPushButton:pressed {
                background-color: #3c476c;
            }
        """)
        main_layout.addWidget(disconnect_button, alignment=Qt.AlignTop | Qt.AlignRight)

        main_layout.addWidget(first_part)

        # Second part of the authenticated page (with scrollable labels)
        second_part = QWidget()
        second_part_layout = QHBoxLayout(second_part)

        # Left part of the second part
        left_scroll_area = QScrollArea()
        left_part_content = QWidget()
        left_part_layout = QVBoxLayout(left_part_content)

        # Add a function to handle label click
        def label_clicked(key):
            controller.clear_layout_labels(right_part_layout)
            self.checkbox_group = QButtonGroup()
            for key, value in json.loads(self.labels_data[key]).items():
                checkbox = QCheckBox("Completed", right_part_content)
                self.checkbox_group.addButton(checkbox)
                checkbox.setStyleSheet("color: #ffffff; font-size: 12pt;")
                right_part_layout.addWidget(checkbox)

                controller.create_label(self, right_part_layout, value,
                                        "color: #ffffff; background-color: #4eafa3; font-size: 24pt; margin: 5px; "
                                        "padding: 5px; border-radius: 10px;")

            self.all_labels = controller.get_labels_in_layout(right_part_layout)

            # Add a View More Button
            view_more_button = QPushButton("View more", self)
            view_more_button.setCursor(QCursor(Qt.PointingHandCursor))
            view_more_button.setStyleSheet(
                "color: #ffffff; background-color: #5766F9; font-size: 12pt; border-radius: 10px; "
                "margin: 5px; padding: 5px;")
            view_more_button.setFixedWidth(100)
            right_part_layout.addWidget(view_more_button, alignment=Qt.AlignBottom | Qt.AlignRight)
            view_more_button.clicked.connect(self.expansion_page)

        for key, value in self.labels_data.items():

            label_step = QPushButton(f"{key}", left_part_content)
            label_step.setStyleSheet("color: #ffffff; background-color: #5766F9; font-size: 12pt; margin: 10px; "
                                     "padding: 5px; border-radius: 10px;")
            label_step.setCursor(QCursor(Qt.PointingHandCursor))
            label_step.clicked.connect(partial(label_clicked, key))
            left_part_layout.addWidget(label_step)

        left_scroll_area.setWidget(left_part_content)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        left_part_content.setStyleSheet("background-color: white;")

        # Add the left scroll area to the second part layout
        second_part_layout.addWidget(left_scroll_area)

        # Right part of the second part
        right_area = QScrollArea()
        right_part_content = QWidget()
        right_part_layout = QVBoxLayout(right_part_content)

        right_area.setWidget(right_part_content)
        right_area.setWidgetResizable(True)
        right_area.setStyleSheet("background-color: white;")
        second_part_layout.addWidget(right_area)

        main_layout.addWidget(second_part)

    # Show a confirmation dialog before disconnecting
    def disconnect(self):
        # Show a confirmation dialog
        reply = QMessageBox.question(self, 'Disconnect', 'Are you sure you want to disconnect?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Close the authenticated page and show the login window
            self.close()
            self.login_window.show()

    def expansion_page(self):
        # This function will be called when the button is clicked
        checked_id = controller.view_more(self.checkbox_group)
        if checked_id:
            # Retrieve and display detailed step content in the expanded visualization page
            step_content = self.all_labels[(int(checked_id) * -1) - 2].text()
            self.expand_visualisation_page = ExpandVisualisationPage(self, step_content)
            self.expand_visualisation_page.show()
            self.hide()


# Define a class for the login window
class LoginWindow(QMainWindow):
    # Center the window on the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()
        # Set up the main window properties
        self.setWindowTitle("ISICOD")
        self.setGeometry(0, 0, 500, 380)  # Set an initial size
        self.center()

        # Load the background image
        background_image = QPixmap('background.jpg')  # Replace 'path_to_image.jpg' with your image file path

        # Create a label to hold the background image
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, background_image.width(), background_image.height())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Replace image paths with your actual image paths
        side_img_1 = QLabel(self)
        side_img_1.setPixmap(QPixmap("side-.png"))
        layout.addWidget(side_img_1)

        controller.create_label(self, layout, "Welcome", "color: #5766F9; font-size: 54pt;")

        controller.create_label(self, layout, "log in to continue...", "color: #7E7E7E; font-size: 12pt;")

        entry_layout = QHBoxLayout()

        controller.create_label(self, entry_layout, "Email:", "color: #5766F9; font-size: 14pt;")

        self.email_entry = QLineEdit(self)
        self.email_entry.setFixedWidth(300)
        entry_layout.addWidget(self.email_entry)
        layout.addLayout(entry_layout)

        entry_layout = QHBoxLayout()
        controller.create_label(self, entry_layout, "Password:", "color: #5766F9; font-size: 14pt;")

        self.password_entry = QLineEdit(self)
        self.password_entry.setFixedWidth(300)
        self.password_entry.setEchoMode(QLineEdit.Password)
        entry_layout.addWidget(self.password_entry)
        layout.addLayout(entry_layout)

        controller.create_label(self, layout, "", "color: #FF0000; font-size: 12pt;")
        controller.create_label(self, layout, "", "color: #FF0000; font-size: 12pt;")

        login_button = QPushButton("Login", self)
        login_button.setStyleSheet("color: #ffffff; background-color: #5766F9; font-size: 12pt; margin: 10px; "
                                   "padding: 5px; border-radius: 10px;")

        login_button.clicked.connect(self.login)
        login_button.setCursor(QCursor(Qt.PointingHandCursor))  # Set cursor to pointing hand
        layout.addWidget(login_button)

        self.data_visualisation_page = DataVisualisation(self)

    def login(self):
        # Attempt to log in when the "Login" button is clicked
        email = self.email_entry.text()
        password = self.password_entry.text()

        # Construct SQL query to fetch user record
        result = model.execute_query(f"SELECT * FROM users WHERE email='{email}' AND password='{password}'", fetch=True)

        # Replace with your actual logic for authentication
        if result:
            self.data_visualisation_page.show()
            self.hide()
            # Clear the entries when valid login
            self.email_entry.clear()
            self.password_entry.clear()
        else:
            # Display a popup for failed login attempts
            controller.show_popup("Login Failed", "Invalid email or password. Please try again.")


if __name__ == '__main__':
    # Instantiate the application and the login window
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
