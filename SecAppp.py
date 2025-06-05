import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import mysql.connector
from datetime import datetime

class SecurityGateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Security Gate Management")
        self.setGeometry(100, 100, 400, 250)

        # Initialize UI
        self.init_ui()
        
        # Initialize database connection
        self.init_database()

    def init_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create input fields
        self.driver_name = QLineEdit()
        self.driver_name.setPlaceholderText("Enter Driver Name")
        self.license_plate = QLineEdit()
        self.license_plate.setPlaceholderText("Enter License Plate Number")
        self.time_period = QLineEdit()
        self.time_period.setPlaceholderText("Enter Time Period (e.g., 2 hours)")

        # Create submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setEnabled(False)
        
        # Add widgets to layout
        layout.addWidget(self.driver_name)
        layout.addWidget(self.license_plate)
        layout.addWidget(self.time_period)
        layout.addWidget(self.submit_button)
        
        # Connect signals
        self.driver_name.textChanged.connect(self.check_inputs)
        self.license_plate.textChanged.connect(self.check_inputs)
        self.time_period.textChanged.connect(self.check_inputs)
        self.submit_button.clicked.connect(self.submit_data)

    def init_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="your_username",  # Replace with your MySQL username
                password="your_password",  # Replace with your MySQL password
                database="security_gate_db"
            )
            self.cursor = self.db.cursor()
            
            # Create table with specified columns
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS gate_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data DATE,
                    time_of_entering DATETIME,
                    driver_name VARCHAR(255),
                    licence_plate VARCHAR(50),
                    how_long VARCHAR(50)
                )
            """)
            self.db.commit()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to database: {err}")
            sys.exit(1)

    def check_inputs(self):
        # Enable submit button only if all fields are filled
        all_filled = (self.driver_name.text().strip() and 
                     self.license_plate.text().strip() and 
                     self.time_period.text().strip())
        self.submit_button.setEnabled(all_filled)

    def submit_data(self):
        driver_name = self.driver_name.text().strip()
        license_plate = self.license_plate.text().strip()
        time_period = self.time_period.text().strip()
        current_date = datetime.now().strftime("%Y-%m-%d")
        entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Insert into MySQL
            query = """
                INSERT INTO gate_records (data, time_of_entering, driver_name, licence_plate, how_long)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (current_date, entry_time, driver_name, license_plate, time_period)
            self.cursor.execute(query, values)
            self.db.commit()

            # Show success message and clear inputs
            QMessageBox.information(self, "Success", "Record added successfully!")
            self.driver_name.clear()
            self.license_plate.clear()
            self.time_period.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Failed to save record: {err}")

    def closeEvent(self, event):
        # Clean up database connection
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SecurityGateApp()
    window.show()
    sys.exit(app.exec())v