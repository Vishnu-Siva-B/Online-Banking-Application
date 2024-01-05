# Importing necessary libraries
import sqlite3
import os
from datetime import datetime
from pytz import timezone
import time


# Function to establish a connection to the SQLite database
def get_db_connection():
    """
    Establishes a connection to the SQLite database.

    Returns:
    - conn: SQLite connection object
    """
    conn = sqlite3.connect(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "bankapp.db")
    )
    conn.row_factory = sqlite3.Row
    return conn


def create_user_table():
    """
    Creates the 'user' table in the database if it does not exist.
    The table contains columns for account details such as account number, password, name, email, location, and balance.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            accNo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            firstName TEXT,
            lastName TEXT,
            email TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            balance INTEGER DEFAULT 1000
        )
    """
    )

    conn.commit()
    conn.close()


def insert_user(accNo, password, firstName, lastName, email, city, state, country):
    """
    Inserts a new user into the 'user' table with default balance set to 1000.

    Args:
    - accNo: Account number
    - password: User password
    - firstName: First name of the user
    - lastName: Last name of the user
    - email: Email address of the user
    - city: City of residence
    - state: State of residence
    - country: Country of residence
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the new user into the database with a default balance of 1000
    cursor.execute(
        """
        INSERT INTO user (accNo, password, firstName, lastName, email, city, state, country, balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (accNo, password, firstName, lastName, email, city, state, country, 1000),
    )

    conn.commit()
    conn.close()


def verify_credentials(accNo, password):
    """
    Verifies user credentials by checking the account number and password.

    Args:
    - accNo: Account number
    - password: User password

    Returns:
    - True if credentials are valid, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user information based on the account number
    cursor.execute("SELECT * FROM user WHERE accNo = ?", (accNo,))
    user = cursor.fetchone()

    conn.close()

    # Verify the password if the user is found
    if user and user["password"] == password:
        return True
    else:
        return False


def is_account_exists(accNo):
    """
    Checks if an account with the given account number already exists.

    Args:
    - accNo: Account number

    Returns:
    - True if the account exists, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE accNo = ?", (accNo,))
    user = cursor.fetchone()

    conn.close()

    return user is not None


def get_user_details(accNo):
    """
    Retrieves user details from the 'user' table based on the account number.

    Args:
    - accNo: Account number

    Returns:
    - Dictionary containing user details (first name, last name, email, city, state, country, balance)
    """
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Example query: Select user details from the table where accNo matches
        cursor.execute(
            "SELECT firstName, lastName, email, city, state, country, balance FROM user WHERE accNo = ?",
            (accNo,),
        )
        user_details = cursor.fetchone()

        if user_details:
            # Assuming the query result is a tuple (firstName, lastName, email, city, state, country)
            user_details_dict = {
                "firstName": user_details[0],
                "lastName": user_details[1],
                "email": user_details[2],
                "city": user_details[3],
                "state": user_details[4],
                "country": user_details[5],
                "balance": user_details[6],
                "accNo": accNo,
            }
            return user_details_dict
        else:
            return None

    except Exception as e:
        print("Error fetching user details:", str(e))
        return None

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


# models.py


def create_transaction_table():
    """
    Creates the 'transactions' table in the database if it does not exist.
    The table contains columns for account number, timestamp, description, amount, and balance.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            accNo TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            amount INTEGER NOT NULL,
            balance INTEGER NOT NULL,
            FOREIGN KEY (accNo) REFERENCES user (accNo)
        )
    """
    )

    conn.commit()
    conn.close()


def update_balance(accNo, amount):
    """
    Updates the user's balance in the 'user' table.

    Args:
    - accNo: Account number
    - amount: Amount to update the balance by
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the user's current balance
    cursor.execute("SELECT balance FROM user WHERE accNo = ?", (accNo,))
    current_balance = cursor.fetchone()["balance"]

    # Update the balance
    new_balance = current_balance + amount
    cursor.execute("UPDATE user SET balance = ? WHERE accNo = ?", (new_balance, accNo))

    conn.commit()
    conn.close()


def record_transaction(accNo, description, amount):
    """
    Records a transaction in the 'transactions' table.

    Args:
    - accNo: Account number
    - description: Transaction description (e.g., deposit, withdrawal)
    - amount: Transaction amount
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the user's current balance
    cursor.execute("SELECT balance FROM user WHERE accNo = ?", (accNo,))
    current_balance = cursor.fetchone()["balance"]

    kolkata_time = datetime.now(timezone("Asia/Kolkata"))
    timestamp = kolkata_time.strftime("Date: %d-%m-%y || Time: %H:%M:%S")

    # Update the transactions table
    cursor.execute(
        """
        INSERT INTO transactions (accNo, timestamp, description, amount, balance)
        VALUES (?, ?, ?, ?, ?)
    """,
        (accNo, timestamp, description, amount, current_balance),
    )

    conn.commit()
    conn.close()


def get_transaction_history(accNo):
    """
    Retrieves the transaction history for a user.

    Args:
    - accNo: Account number

    Returns:
    - List of transactions (each transaction is a dictionary)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch transactions for the user
    cursor.execute(
        "SELECT * FROM transactions WHERE accNo = ? ORDER BY timestamp DESC", (accNo,)
    )
    transactions = cursor.fetchall()

    conn.close()

    return transactions
