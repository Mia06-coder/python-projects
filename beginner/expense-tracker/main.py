import os
import sqlite3
import argparse
import logging
from datetime import datetime
from rich.console import Console

# Set up logging for error tracking
logging.basicConfig(
    filename = "expense_tracker.log",
    level = logging.ERROR,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

#  Set up script directory and database file path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "expenses.db")

# Initialize Rich console for styled CLI output
console = Console()

class ExpenseTracker:
    """
    A class for tracking expenses using an SQLite database.

    This class provides methods to initialize a database, store expense records, and manage 
    user transactions efficiently.

    Attributes:
        None

    Methods:
        create_db(): Creates the expenses database table if it does not exist.
        add_expense(description: str, amount: float): Adds a new expense entry to the database.
    """

    def __init__(self):
        """
        Initializes the ExpenseTracker instance.

        Ensures that the database and required tables exist before performing any operations.
        """
        self.create_db()

    def create_db(self) -> None:
        """
        Creates the expenses table in the SQLite database if it does not already exist.

        The table consists of:
            - id: Auto-incremented primary key.
            - date: Date of the expense.
            - description: Description of the expense.
            - amount: Monetary value of the expense.

        If the table does not exist, it is created. Otherwise, no changes are made.
        
        Logs an error if a database-related issue occurs.
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                
                # Validate if table exists
                cursor.execute("PRAGMA table_info(expenses)")
                columns = cursor.fetchall()

                if not columns:  # If the table doesn't exist
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL
                    )
                    ''')
                    conn.commit()
                    console.print("[green]Database initialized successfully.[/]")
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            console.log(f"[bold red]Database initialization error: {e}[/]")

    def add_expense(self, description: str, amount: float) -> None:
        """
        Adds an expense to the database.

        Parameters:
            description (str): A brief description of the expense.
            amount (float): The monetary amount of the expense.

        The expense is stored in the database with the current date. 

        Outputs:
            - A success message if the expense is added successfully.
            - An error message if the description is empty or the amount is not positive.

        Raises:
            ValueError: If `description` is empty or `amount` is not greater than zero.
            sqlite3.Error: If there is an issue inserting data into the database.
        """
        if not description.strip():
            console.print("[bold red]Error: Description cannot be empty.[/]")
            return
        
        if amount <= 0:
            console.print("[bold red]Error: Amount must be greater than zero.[/]")
            return
        
        try:
            date = datetime.now().strftime("%Y-%m-%d")  # Store date as 'YYYY-MM-DD'
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()

                # Insert expense data into database
                cursor.execute("INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)", 
                                    (date, description, amount))
                conn.commit()
                console.print(f"[green]Expense added successfully: {description} - ${amount}[/]")
        except sqlite3.Error as e:
            logging.error(f"Error adding expense: {e}")
            console.log(f"[bold red]Error adding expense: {e}[/]")

def main() -> None:
    """
    Main function to handle user input and manage expense tracking via CLI.

    This function sets up an argument parser, allowing users to add new expenses 
    via command-line arguments. It initializes an instance of `ExpenseTracker` and 
    calls the appropriate method based on the user’s input.

    Commands:
        - `add`: Adds a new expense.
            Arguments:
                --description: The description of the expense (required).
                --amount: The amount spent (required, must be a float).
    
    If no valid command is provided, the help message is displayed.
    """
    tracker = ExpenseTracker()

    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add expense command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--description", required=True, help="Description of the expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Expense amount")

    args = parser.parse_args()

    if args.command == "add":
        tracker.add_expense(args.description, args.amount)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()