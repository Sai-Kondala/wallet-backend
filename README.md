# wallet-backend

A secure transactional wallet backend built using **Python Flask** and **SQLite**.

This project simulates the core backend behavior of digital wallet/payment systems.

---

## Features

- User Registration
- Secure Login (Password Hashing)
- Session Token Authentication
- Token Expiry & Logout
- Check Account Balance
- Deposit Funds
- Transfer Money Between Users
- Transaction History (Ledger/Passbook)
- Atomic Transactions (No money loss)

---

## Tech Stack

- Python 3
- Flask
- SQLite
- Werkzeug Security

---

## System Design Concepts Implemented

- Authentication vs Authorization
- Session Management
- Atomic Database Transactions
- Rollback Safety
- Ledger-based Accounting
- UTC Time Handling

---

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| /register | POST | Create new user |
| /login | POST | Login and receive token |
| /balance | POST | Check wallet balance |
| /deposit | POST | Add money |
| /transfer | POST | Send money |
| /transactions | POST | Transaction history |
| /logout | POST | End session |

---

## Example Workflow

1. Register user
2. Login and receive token
3. Deposit money
4. Transfer to another user
5. View transaction history

---

## Important Behaviors

- Passwords are hashed (never stored in plain text)
- Transfers are atomic (no partial transactions)
- Tokens expire automatically
- Ledger stores complete transaction history

---

## Running the Project

```bash
pip install flask
python3 app.py
```

Server starts at:

```
http://127.0.0.1:5000
```

---

## Project Goal

To understand how backend systems for payment applications work internally, including authentication, data consistency, and financial transaction safety.