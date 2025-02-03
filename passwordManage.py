from cryptography.fernet import Fernet
import sqlite3
import getpass
import os

# Generate and save the encryption key (Run this only once)
def generate_key():
    """Generate an encryption key only if it does not already exist."""
    if os.path.exists("secret.key"):
        print("🔑 Encryption key already exists. Skipping key generation.")
        return  # Exit without generating a new key
    
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    
    print("Encryption key generated successfully!")

# Load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt password
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode())

# Decrypt password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password).decode()

# Initialize database
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

# Save password to database
def save_password(service, username, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",
                   (service, username, encrypted_password))
    conn.commit()
    conn.close()
    print("Password saved successfully!")

# Retrieve password
def retrieve_password(service):
    key = load_key()
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE service = ?", (service,))
    result = cursor.fetchone()
    conn.close()

    if result:
        username, encrypted_password = result
        decrypted_password = decrypt_password(encrypted_password, key)
        print(f"Service: {service}\nUsername: {username}\nPassword: {decrypted_password}")
    else:
        print("No password found for this service.")

# Delete password
def delete_password(service):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE service = ?", (service,))
    conn.commit()
    conn.close()
    print("Password deleted successfully!")

# Main menu
def main():
    init_db()

    while True:
        print("\nPassword Manager")
        print("1. Save Password")
        print("2. Retrieve Password")
        print("3. Delete Password")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")  # Secure password input
            save_password(service, username, password)
        elif choice == "2":
            service = input("Enter service name: ")
            retrieve_password(service)
        elif choice == "3":
            service = input("Enter service name: ")
            delete_password(service)
        elif choice == "4":
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
if __name__ == "__main__":
    # Run this line only once to generate an encryption key
    generate_key()

    main()
