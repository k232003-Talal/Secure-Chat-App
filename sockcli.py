import socket
import threading
import filing
import time
import os           #for forcefully terminate script if connection is closed.
import platform     #different commands needed on windows and linux
import sys          #to ask python to run the script again
import queue
import msg_security

class ChatApplication:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.listener_socket = None
        self.client_socket = None
        self.sender_socket = None
        self.listening = False
        self.listen_thread = None
        self.target_ip = None
        self.message_queue = queue.Queue()  # <-- Message queue
        self.sending_thread = threading.Thread(target=self.send_message_from_queue, daemon=True)
        self.sending_thread.start()  # <-- Start the sending thread

    def exit_program(self, quit=0):
        """Cleanup sockets and exit"""
        print("Closing sockets and exiting...")
        if self.client_socket:
            self.client_socket.close()
        if self.sender_socket:
            self.sender_socket.close()
        if self.listener_socket:
            self.listener_socket.close()
        
        if quit != 1:
          time.sleep(2)
         
        # Proprly quote Python executable path on Windows
          if platform.system() == "Windows":
             os.startfile(sys.argv[0])
             os._exit(0)
          else:
             python = sys.executable
             os.execl(python, python, *sys.argv)

        else:
          os._exit(0)

    def start_listening(self,my_username):
        """Start the listening socket on a separate thread"""
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
            self.exit_program()

    def _listen_for_messages(self, my_username):
        """Background thread that listens for incoming messages"""
        try:
            self.client_socket, client_address = self.listener_socket.accept()
            print(f"Connected to {client_address}")

            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    print("\nConnection closed by the other user. Exiting...")
                    self.exit_program()

                decrypted_msg=msg_security.RSA_decrypt(data.decode('utf-8'),my_username)
                other_user=filing.get_other_Username(my_username)
                filing.append_msg_chat(decrypted_msg,other_user)

        except (socket.error, ConnectionResetError):
            print("\nConnection lost. Exiting...")
            self.exit_program()
        except Exception as e:
            print(f"Error while listening: {e}")
            self.exit_program()

    def connect_to_target(self, target_ip):
        """Try to establish a connection to the target IP"""
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
                pass  # Continue retrying

    def queue_message(self, message):
        """Add a message to the queue (to be sent when the send button is clicked)."""
        self.message_queue.put(message)       

    def send_message_from_queue(self):
        """Continuously check the queue and send messages when available."""
        while True:
            message = self.message_queue.get()  # Wait until a message is available
            if not self.target_ip or not self.sender_socket:
                print("Not connected to a target.")
                continue  # Skip sending if no connection

            try:
                self.send_message(message)
                print(f"Sent: {message}")
            except (socket.error, ConnectionResetError):
                print("Connection lost while sending message. Exiting...")
                self.exit_program()
            except Exception as e:
                print(f"Error sending message: {e}")    

    def send_message(self, message):
        """Send a message to the connected target"""
        if not self.target_ip or not self.sender_socket:
            print("Not connected to a target.")
            return False
        
        try:
            self.sender_socket.sendall(message.encode('utf-8'))
            return True
        except (socket.error, ConnectionResetError):
            print("Connection lost while sending message. Exiting...")
            self.exit_program()
        except Exception as e:
            print(f"Error sending message: {e}")
            return False




def start_chat_sockets(Username):
    chat_instance = ChatApplication()
    chat_instance.start_listening(Username)  
    other_user=filing.get_other_Username(Username)
    target_ip = filing.get_User_ip(other_user)
    chat_instance.connect_to_target(target_ip)
    return chat_instance #to chat.py
    
        



# if __name__ == "__main__":
#     chat = ChatApplication()
    
#     my_ip = filing.get_User_ip("Talal")
#     print(f"\nYour IP address is: {my_ip}")
    
#     chat.start_listening()  

#     target_ip = filing.get_User_ip("Dani")
#     chat.connect_to_target(target_ip)

#     while True:
#           try:  
#             message = input("Enter message (or 'quit' to exit): ")
#           except EOFError:
#             continue
            
#           if message.lower() == 'quit':
#                 print("You have chosen to exit. Goodbye!")
#                 chat.exit_program(quit=1)
                
#           if not chat.send_message(message):
#                 print("Message sending failed.")