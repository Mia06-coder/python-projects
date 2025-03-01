import os
import sqlite3
import argparse
import logging
import calendar
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

    def list_expenses(self):
        """
        Retrieves and displays all recorded expenses from the database.

        This method fetches all the expenses stored in the database and prints them 
        in a user-friendly, formatted table. If no expenses are found, it notifies 
        the user that there are no records.

        Outputs:
            - A formatted table displaying the expense records, including:
                - ID: Unique identifier of the expense.
                - Date: Date of the expense.
                - Description: Description of the expense.
                - Amount: Amount spent, displayed in dollars.
            - A message if no expenses are recorded.
            - None

        Raises:
            - sqlite3.Error: If an error occurs while interacting with the database.
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, date, description, amount FROM expenses")
                expenses = cursor.fetchall()

                if not expenses:
                    console.print("[yellow]No expenses recorded yet.[/]")
                    return
                
                console.print("[white]=[/]" * 70)
                console.print(f"[cyan]{'ID':<5} {'Date':<15}  {'Description':<35}  {'Amount':<8}[/]")  
                console.print("[white]-[/]" * 70)
                for expense in expenses:
                    # Convert the date string to a datetime object and format it
                    date_obj = datetime.strptime(expense[1], "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d-%b-%Y").upper()  

                    console.print(f"[white]{expense[0]:<5} {formatted_date:<15}  {expense[2]:<35}  ${expense[3]:>8.2f}[/]")
                console.print(f"[bold cyan]\n({len(expenses)})[/]")
        except sqlite3.Error as e:
            logging.error(f"Error fetching expenses: {e}")
            console.log(f"[bold red]Database error: {e}[/]")

    def get_total_expenses(self, month:int = None) -> None:
        """
        Retrieves and displays the total sum of all recorded expenses.

        This method calculates the total expenses from the database by summing up 
        all the amounts in the `expenses` table. If a specific month is provided, 
        it filters expenses for that month only. If no expenses are recorded, 
        it notifies the user. Otherwise, it displays the total amount in a formatted style.

        Args:
        month (int, optional): The month (1-12) for which expenses should be retrieved. 
                               Defaults to None, which retrieves all expenses.

        Outputs:
            - The total expenses, formatted as a monetary value (e.g., $123.45).
            - A message if no expenses have been recorded.
            - None

        Raises:
            - sqlite3.Error: If an error occurs while interacting with the database.
        """
        try:
            # Validate month input
            if month is not None and (month < 1 or month > 12):
                console.print("[bold red]Invalid month. Please provide a value between 1 and 12.[/]")
                return
            
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()

                if month is not None:
                    # Convert month number to month name
                    month_name = calendar.month_name[month]

                    # Query for expenses in the specified month
                    cursor.execute("SELECT SUM(amount) FROM expenses WHERE strftime('%m', date)=?", (f"{month:02d}",))
                    total_expenses = cursor.fetchone()[0]
                else:
                    # Query for all expenses
                    cursor.execute("SELECT SUM(amount) FROM expenses")
                    total_expenses = cursor.fetchone()[0]

                # If there are no expenses are recorded
                if total_expenses is None:
                    console.print("[yellow]No expenses recorded yet.[/]")
                    return

                # Display the total expenses 
                if month is not None:
                    console.print(f"\nTotal expenses for the month of {month_name}: [bold cyan]${total_expenses:.2f}[/]")
                else:
                    console.print(f"\nTotal expenses: [bold cyan]${total_expenses:.2f}[/]")
        
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            console.log(f"[bold red]Database error: {e}[/]")

    def check_id(self, cursor,expense_id:int) -> tuple[bool,tuple|None]:
        # Check if the expense ID exists directly in the database
        cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
        expense = cursor.fetchone()

        # If the ID doesn't exist, print a message and return
        if not expense:
            console.print("[yellow]Expense ID not found.[/]")
            return False, None
        
        return True, expense

    def delete_expense(self, expense_id:int) -> None:
        """
        Deletes an expense from the database based on the provided expense ID, and logs the deleted expense to a file for record-keeping.

        This method checks if the specified expense ID exists in the database. If 
        the ID is found, the corresponding expense record is deleted and logged. If the ID 
        doesn't exist, a message is displayed notifying the user.

        Parameters:
            expense_id (int): The ID of the expense to be deleted.

        Outputs:
            - A message indicating whether the deletion was successful or if the ID was not found.
            - None

        Raises:
            - sqlite3.Error: If an error occurs while interacting with the database.
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()

                id_found, expense = self.check_id(cursor,expense_id)
                    
                if not id_found:
                    return
                
                # If the ID is valid, proceed to delete the expense
                # Format the log message
                deleted_expense_log = f"{expense_id}: {expense[1]} - {expense[2]} - ${expense[3]:.2f} - {datetime.now().strftime('%d %b %Y %H:%M:%S')}\n"
                # Append the deleted expense to a log file
                with open("deleted_expenses.log", "a") as log_file:
                    log_file.write(deleted_expense_log)

                # Delete the expense from the database
                cursor.execute("DELETE FROM expenses WHERE id=?",(expense_id,))
                conn.commit()

                # Notify the user that the expense was successfully deleted
                console.print("[green]Expense successfully deleted![/]")

        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            console.log(f"[bold red]Database error: {e}[/]")

    def update_expense(self, expense_id: int, amount: float = None, description: str = None, date: str = None) -> None:
        """
        Updates an existing expense in the database based on the provided expense ID.

        This method allows the user to update the amount, description, and date of an expense. 
        If no valid update fields are provided, a message is displayed, and no changes are made.
        It also logs the updates made to an expense in a log file for future reference.

        Args:
            expense_id (int): The ID of the expense to be updated.
            amount (float, optional): The new amount for the expense.
            description (str, optional): The new description of the expense.
            date (str, optional): The new date of the expense (format: YYYY-MM-DD).

        Outputs:
            - A success message if the expense is updated.
            - A message if no updates are made.
            - Logs the update in a file for record-keeping.
            - None
            
        Raises:
            - sqlite3.Error: If an error occurs during database interaction.
        """
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()

                # Check if the expense ID exists in the database
                id_found, expense = self.check_id(cursor,expense_id)

                # If the ID does not exist, return without updating
                if not id_found:
                    return
                
                # To check if any changes were actually made
                original_amount = expense[3]
                original_description = expense[2]
                original_date = expense[1]
                
                updates = []
                params = []

                # Validate and update the date if provided
                if date is not None:
                    if not validate_date(date):
                        console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/]")
                        return
                    updates.append("date=?")
                    params.append(date)

                if amount is not None:
                    updates.append("amount=?")
                    params.append(amount)

                if description is not None:
                    updates.append("description=?")
                    params.append(description)

                # If no updates were provided, notify the user and return
                if not updates:
                    console.print("[yellow]No changes provided. Nothing to update.[/]")
                    return
                
                params.append(expense_id)

                # Create the SQL UPDATE query dynamically based on the provided fields
                update_query = f"UPDATE expenses SET {', '.join(updates)} WHERE id=?"               
                cursor.execute(update_query, tuple(params))
                conn.commit()

                # Log the details of the update for record-keeping
                updated_log = f"Updated Expense ID {expense_id} - {datetime.now().strftime('%d %b %Y %H:%M:%S')}: "
                if amount is not None and original_amount != amount:
                    updated_log += f"Amount: ${expense[3]:.2f} -> ${amount:.2f}, "
                if description is not None and original_description != description:
                    updated_log += f"Description: '{expense[2]}' -> '{description}', "
                if date is not None and original_date != date:
                    updated_log += f"Date: {expense[1]} -> {date}, "
                
                updated_log = updated_log.rstrip(", ") + "\n"

                # Append the updated expense to a log file
                with open("update_expenses.log", "a") as log_file:
                    log_file.write(updated_log)

                # Notify the user that the expense was successfully updated
                console.print("[green]Expense successfully updated![/]")
            
                # Log success for auditing
                logging.info(f"Expense ID {expense_id} successfully updated.")
        
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            console.log(f"[bold red]Database error: {e}[/]")

def validate_date(date_str: str) -> bool:
        try:
            # Try to parse the date string into a datetime object
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            # If a ValueError occurs, the date format is invalid
            return False
        
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

    # Add expense command configuration
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--description", required=True, help="Description of the expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Expense amount")

    # Command to list all recorded expenses
    subparsers.add_parser("list", help="List all recorded expenses")

    # Command to get the summary of total expenses
    summary_parser = subparsers.add_parser("summary", help="Displays the total amount of recorded expenses")
    summary_parser.add_argument("--month", type=int, help="Month of the expense was made")

    # Delete expense command configuration
    delete_parser = subparsers.add_parser("delete", help="Delete expense by its ID")
    delete_parser.add_argument("--id",type=int, required=True, help="ID of the expense to delete")
    
    # Update expense command configuration
    update_parser = subparsers.add_parser("update", help="Update expense by its ID")
    update_parser.add_argument("--id",type=int, required=True, help="ID of the expense to update")
    update_parser.add_argument("--amount", type=float, help="New expense amount")
    update_parser.add_argument("--description", type=str, help="New description for the expense")
    update_parser.add_argument("--date", type=str, help="New date of the expense (YYYY-MM-DD)")

    args = parser.parse_args()

    if args.command == "add":
        tracker.add_expense(args.description, args.amount)
    elif args.command == "list":
        tracker.list_expenses()
    elif args.command == "summary":
        tracker.get_total_expenses(args.month)
    elif args.command == "delete":
        tracker.delete_expense(args.id)
    elif args.command == "update":
        tracker.update_expense(args.id, args.amount, args.description, args.date)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()