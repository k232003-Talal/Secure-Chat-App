# Secure Encrypted Chat Application (Desktop)

This project is a secure, user-friendly desktop chat application built with Python's Tkinter, socket programming, and end-to-end RSA encryption. It provides login authentication, password management, encrypted real-time messaging, and IP address management via Firebase.

---

## Chat Implementation Details

- The chat window does not appear until the connection is established.  
- Both users attempt to connect continuously until a connection is made.  
- Once the connection is established, the chat window appears for both users.  
- Either user can send messages.  
- If one user closes the chat, it automatically closes for the other user as well.

---

## Features

### User Authentication

- Secure login system with password validation.  
- Basic test credentials:  
  - Username: Talal or Dani  
  - Password: test1234

### Password Management

Users can change their passwords with the following validation checks:

- Minimum and maximum length  
- Prevention of old password reuse  
- Required confirmation matching  
- Blocking of invalid characters

### End-to-End Encrypted Messaging

- RSA encryption ensures private communication between users.  
- Messages are encrypted, serialized, and transmitted over TCP sockets.  
- The `ChatApplication` class handles two main sockets:  
  - A listener socket for receiving messages  
  - A sender socket for delivering messages asynchronously using a queue

### Real-Time Chat Updates

- The chat window refreshes in real-time using Tkinter’s `after()` scheduler.  
- It checks the chat log file and updates the display every second if changes are found.  
- User messages are visually distinguished in the chat for better clarity.

### Dynamic IP Management with Firebase

- Public IP addresses are updated dynamically in a Firebase Realtime Database.  
- This allows communication to continue even if the user’s IP address changes (e.g., due to network switch or device change).  
- IP addresses are fetched and updated to maintain reliable peer-to-peer connectivity.

---

## Tech Stack

- Python  
- Tkinter (GUI)  
- Sockets and Threads (Network Communication)  
- RSA Encryption (via custom `msg_security` module)  
- Firebase Realtime Database (for IP Management)  
- Pickle (for Message Serialization)

---

## Project Structure Overview


project/
│
├── main.py               # Main logic and interface
├── chat.py               # Chat functionality & message encryption
├── filing.py             # File operations (usernames, passwords)
├── database_updator.py   # Firebase-based IP synchronization
├── sockcli.py            # Socket client for encrypted chat
├── msg_security.py       # RSA encryption and decryption logic
├── design.py             # Styling and UI constants
└── README.md             # Project documentation

---

## How It Works

1. **Login** – Users enter their credentials to access their account.  
2. **Dashboard** – After login, users can start a chat, update IP, or change their password.  
3. **Chat** – Messages are encrypted and sent over a secure socket.  
4. **Live Updates** – The interface refreshes automatically using file-based change detection.  
5. **IP Sync** – When the user’s IP changes, it's updated to Firebase to maintain connectivity.

---

## Test Credentials

- Username: Talal  
  Password: test1234

- Username: Dani  
  Password: test1234

---

## Security Highlights

- RSA encryption ensures end-to-end confidentiality.  
- Communication over sockets is encrypted and handled using isolated threads.  
- Passwords are securely masked and validated to avoid weak credentials.

---

## Installation Notes

Replace the local database URL with Your database URL in database_updator.py
Place your database credentials file in the same directory.
Also change the database credentials filepath (design.py).
You will also find these instructions in database_updator.py.

Also Ensure the following packages are installed:

```bash
pip install firebase-admin
pip install sympy
pip install requests
