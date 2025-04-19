import socket
import threading
import filing
import pickle
import queue
import msg_security

""" The ChatApplication class manages two primary sockets: a listener socket for receiving messages and a sender socket for sending messages to a target IP.
    When a user starts listening, it binds the listener socket to the specified host and port, then spawns a separate thread to listen for incoming connections. 
    For outgoing communication, it places messages in a queue, which are processed by another thread to ensure messages are sent asynchronously. When connected,
    messages are serialized with pickle, encrypted with RSA (through msg_security), and sent to the target. If a connection is lost or the chat window is closed,
     the sockets are properly shut down, and the chat window is terminated. """

class ChatApplication:
    def __init__(self, host='0.0.0.0', port=5555, chat_window=None):
        self.host = host
        self.port = port
        self.listener_socket = None
        self.client_socket = None
        self.sender_socket = None
        self.listening = False
        self.listen_thread = None
        self.target_ip = None
        self.chat_window = chat_window
        self.message_queue = queue.Queue()
        self.sending_thread = threading.Thread(target=self.send_message_from_queue, daemon=True)
        self.sending_thread.start()

    def close_chat_window(self):
        print("Connection terminated. Chat closed.\n ----------------------------------> Ignore the error(s) below. The error occurs because the chat widget is being updated by the scheduler while it is being closed.\n ----------------------------------> Once the chat is reopened, the updates will proceed normally.")

        try:
            if self.client_socket:
                self.client_socket.close()
            if self.sender_socket:
                self.sender_socket.close()
            if self.listener_socket:
                self.listener_socket.close()
        except:
            pass

        if self.chat_window:
            self.chat_window.after(0, self.chat_window.destroy)
   

    def start_listening(self, my_username):
        if self.listening:
            return

        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.listener_socket.bind((self.host, self.port))
            self.listener_socket.listen(1)
            self.listening = True
            self.listen_thread = threading.Thread(target=self._listen_for_messages, args=(my_username,))
            self.listen_thread.daemon = True
            self.listen_thread.start()
            print(f"Started listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"Error starting listener: {e}")
            self.close_chat_window()

    def _listen_for_messages(self, my_username):
        try:
            self.client_socket, client_address = self.listener_socket.accept()
            print(f"Connected to {client_address}")

            while True:
                data = self.client_socket.recv(4096)
                if not data:
                    print("Connection closed by the other user.")
                    self.close_chat_window()
                    break

                received_obj = pickle.loads(data)
                decrypted_msg = msg_security.RSA_decrypt(received_obj, my_username)
                if decrypted_msg == "__CLOSE__":
                    print("Received close signal from other user.")
                    self.close_chat_window()
                    break
                other_user = filing.get_other_Username(my_username)
                filing.append_msg_chat(decrypted_msg, other_user)

        except (socket.error, ConnectionResetError):
            print("Connection lost.")
            self.close_chat_window()
        except Exception:         #if connection closed, withdraw chat window.
            self.close_chat_window()

    def connect_to_target(self, target_ip):
        self.target_ip = target_ip

        while True:
            if self.sender_socket:
                self.sender_socket.close()

            self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sender_socket.settimeout(5)

            try:
                print(f"Trying to connect to {target_ip}:{self.port}...")
                self.sender_socket.connect((target_ip, self.port))
                print(f"Connected to {target_ip} for sending messages")
                self.sender_socket.settimeout(None)
                return
            except (socket.timeout, socket.error):
                pass  # Retry silently

    def queue_message(self, message):
        self.message_queue.put(message)

    def send_message_from_queue(self):
        while True:
            message = self.message_queue.get()
            if not self.target_ip or not self.sender_socket:
                print("Not connected to a target.")
                continue

            try:
                self.send_message(message)
                print(f"Sent: {message}")
            except (socket.error, ConnectionResetError):
                print("Connection lost while sending message.")
                self.close_chat_window()
            except Exception as e:
                print(f"Error sending message: {e}")
                self.close_chat_window()

    def send_message(self, message):
        if not self.target_ip or not self.sender_socket:
            print("Not connected to a target.")
            return False

        try:
            data = pickle.dumps(message)
            self.sender_socket.sendall(data)
            return True
        except (socket.error, ConnectionResetError):
            print("Connection lost while sending message.")
            self.close_chat_window()
            return False
        except Exception as e:
            print(f"Error sending message: {e}")
            self.close_chat_window()
            return False


def start_chat_sockets(Username, chat_window):
    chat_instance = ChatApplication(chat_window=chat_window)
    chat_instance.start_listening(Username)
    other_user = filing.get_other_Username(Username)
    target_ip = filing.get_User_ip(other_user)
    chat_instance.connect_to_target(target_ip)
    return chat_instance
