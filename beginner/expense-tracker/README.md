# **Expense Tracker** 📊

## **Description of Tech and Why**

This project is built using **Python**, leveraging its ease of use, extensive libraries, and strong support for data handling. It uses:

- `rich` – For better CLI output visualization.
- `sqlite3` – To store and manage expense records efficiently.
- `argparse` – To handle user inputs in a structured manner.

Python was chosen due to its simplicity, readability, and strong ecosystem for automation and data processing.

---

## **Table of Contents**

- [How the Project Came About](#how-the-project-came-about)
- [Motivation Behind It](#motivation-behind-it)
- [Features](#features)
- [Usage](#usage)
- [Limitations](#limitations)
- [Challenges](#challenges)
- [What Problems It Hopes to Solve](#what-problems-it-hopes-to-solve)
- [Intended Use](#intended-use)
- [Credits](#credits)

---

## **How the Project Came About**

This project is part of my **Python learning journey**. I’m following the **roadmap.sh** Python roadmap, and this expense tracker is one of the recommended projects ([see project](https://roadmap.sh/projects/expense-tracker)). It provides hands-on experience in working with **data storage, CLI applications, and user input handling**.

## **Motivation Behind It**

I wanted to build a **practical, real-world application** that enhances my understanding of **Python, databases, and command-line interactions**. Managing expenses is a common task, and creating a tracker helps solidify my skills while solving a useful problem.

## Features

- **Add Expenses**: Record new expenses with a description and amount.
- **List Expenses**: View all recorded expenses with a formatted table.
- **Summary**: Get a total of all recorded expenses.
- **Delete Expenses**: Remove expenses from the database by ID, with all deletions logged for audit purposes.

## **Usage**

### **Installation**

1. Clone this repository:

```sh
git clone https://github.com/Mia06-coder/python-projects/beginner/expense-tracker.git
cd expense-tracker
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

### **Running the Project**

Start the tracker by running:

```sh
python main.py
```

For help with available commands:

```sh
python main.py --help
```

### **Example Usage**

To add an expense:

```sh
python main.py add --description "Monthly Netflix Subscription" --amount 15.99
```

To list all recorded expenses:

```sh
python main.py list
```

To view the total expenses:

```sh
python main.py summary
```

To delete an expense

```sh
python main.py delete --id 5

```

---

## **Limitations**

- **No graphical interface (GUI)** – Currently CLI-based. A web or mobile version could be a future improvement.
- **Basic features** – The project focuses on core expense tracking without advanced analytics.

## **Challenges**

- **Database Handling** – Learning how to structure and manage an SQLite database.
- **Error Handling** – Implementing robust checks to prevent invalid inputs.

## **What Problems It Hopes to Solve**

✅ Helps users **record and categorize** their expenses easily.  
✅ Provides **quick expense summaries** via CLI commands.  
✅ Encourages **better financial tracking** through structured data logging.

## **Intended Use**

This expense tracker is designed for **individuals who prefer a simple, CLI-based solution** for tracking daily expenses.

## **Credits**

Developed by **[Mia Mudzingwa](https://linkedin.com/in/mia-mudzingwa)** as part of my Python learning journey.  
Inspired by **[roadmap.sh](https://roadmap.sh/projects/expense-tracker)**.
