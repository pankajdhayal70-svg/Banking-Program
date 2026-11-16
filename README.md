# Bank Program (CLI)

A lightweight, terminal-based multi-user banking system built in **Python** using **JSON** for local data persistence—no external dependencies required.

## Features

* **Multi-User Support:** Register and log into separate user accounts.
* **Core Transactions:** Deposit, withdraw (with overdraft protection), and transfer funds between users.
* **Transaction History:** Tracks account activity and balances automatically.
* **JSON Storage:** Saves all user data and logs locally across sessions.

## Project Structure

```text
Bank-Program/
├── main.py         # CLI menu & entry point
├── Banker.py       # Banking logic & JSON handling
└── README.md