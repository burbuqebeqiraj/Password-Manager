# Password Manager

## Overview
The **Password Manager** is a simple yet secure console-based application  that allows users to securely store, retrieve, and delete their passwords using encryption. It utilizes the cryptography library to encrypt passwords and store them in an SQLite database (passwords.db). The program ensures that passwords are only accessible when the correct decryption key is provided.

## Features
- Save Password: Store service, username, and encrypted password.
- Retrieve Password: Fetch the username and decrypted password for a specific service.
- Delete Password: Remove stored credentials for a specific service.
- Encryption: Passwords are encrypted using Fernet from the cryptography library to ensure secure storage.

## Technologies Used
- Python
- Cryptography (Fernet Encryption)
- SQLite3 (Database)

## Installation
### Prerequisites
Ensure you have Python installed (version 3.6 or later). Install dependencies using:
```
pip install cryptography
```

### Usage
1. **Generate Encryption Key (First-Time Setup)**

The application requires a secret key (secret.key) to encrypt and decrypt passwords. If the key does not exist, it will be generated automatically.

2. **Run the Password Manager**

```
python passwordManage.py
```

3. **Menu Options**
    - Save Password: Stores a new password securely.
    - Retrieve Password: Retrieves and decrypts a stored password.
    - Delete Password: Removes a password entry.
    - Exit: Closes the application.

### Database Structure

The SQLite database (passwords.db) contains a single table:
```
CREATE TABLE passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
```

## Important Notes

The encryption key (secret.key) is crucial for decrypting your passwords. Do not delete it, and make backups if necessary.
The program will not work if secret.key is lost or deleted, as encrypted passwords cannot be decrypted without it.

## License
This project is open-source and available under the MIT License.
