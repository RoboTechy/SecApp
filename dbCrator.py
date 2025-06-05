import mysql.connector
from mysql.connector import Error

def create_database_and_table():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password"  # Replace with your MySQL password
        )
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS security_gate_db")
        print("Database 'security_gate_db' created or already exists.")

        # Switch to the database
        cursor.execute("USE security_gate_db")

        # Create gate_records table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS gate_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATE NOT NULL,
            time_of_entering DATETIME NOT NULL,
            driver_name VARCHAR(255) NOT NULL,
            licence_plate VARCHAR(50) NOT NULL,
            how_long VARCHAR(50) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table 'gate_records' created or already exists.")

        # Commit changes
        connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    create_database_and_table()