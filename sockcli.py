import socket
import threading
import time

class ChatApplication:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.listener_socket = None
        self.client_socket = None
        self.sender_socket = None
        self.listening = False
        self.connected = False
        self.listen_thread = None
        self.target_ip = None
        
    def start_listening(self):
        """Start the listening socket on a separate thread"""
        if self.listening:
            print("Already listening")
            return
        
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.listener_socket.bind((self.host, self.port))
            self.listener_socket.listen(1)
            self.listening = True
            
            # Start the listening thread
            self.listen_thread = threading.Thread(target=self._listen_for_messages)
            self.listen_thread.daemon = True
            self.listen_thread.start()
            
            print(f"Started listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"Error starting listener: {e}")
            if self.listener_socket:
                self.listener_socket.close()
                self.listener_socket = None
    
    def _listen_for_messages(self):
        """Background thread that listens for incoming messages"""
        print("Waiting for connection...")
        try:
            client_socket, client_address = self.listener_socket.accept()
            self.client_socket = client_socket
            self.connected = True
            print(f"Connected to {client_address}")
            
            
            while self.listening and self.connected:
                try:
                    # Receive data with a timeout to allow checking if we're still listening
                    self.client_socket.settimeout(0.5)
                    data = self.client_socket.recv(1024)
                    
                    if not data:
                        print("Connection closed by sender")
                        self.connected = False
                        break
                    
                    # Display the message
                    message = data.decode('utf-8')
                    print(f"\nReceived: {message}")
                    print("Enter message (or 'quit' to exit): ", end='', flush=True)
                        
                except socket.timeout:
                    # This is just to check if we should still be listening
                    continue
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break
                
        except Exception as e:
            if self.listening:  # Only show error if we didn't stop listening intentionally
                print(f"Error while listening: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
            self.connected = False
            
            # Start listening again to accept new connections
            if self.listening:
                # Create a new listener socket since the old one is closed on accept()
                self._restart_listener()
    
    def _restart_listener(self):
        """Restart the listener socket after a connection ends"""
        if self.listener_socket:
            self.listener_socket.close()
            
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.listener_socket.bind((self.host, self.port))
            self.listener_socket.listen(1)
            print(f"Restarted listening on {self.host}:{self.port}")
        except Exception as e:
            print(f"Error restarting listener: {e}")
            self.listener_socket.close()
            self.listener_socket = None
            self.listening = False
    
    def connect_to_target(self, target_ip):
        """Establish a persistent connection to the target for sending messages"""
        if self.sender_socket:
            # Close existing connection first
            self.sender_socket.close()
            
        self.target_ip = target_ip
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            print(f"Connecting to {target_ip}:{self.port}...")
            self.sender_socket.connect((target_ip, self.port))
            print(f"Connected to {target_ip} for sending messages")
            return True
        except Exception as e:
            print(f"Error connecting to target: {e}")
            self.sender_socket = None
            return False
    
    def send_message(self, message):
        """Send a message to the connected target"""
        if not self.target_ip or not self.sender_socket:
            print("Not connected to a target. Call connect_to_target first.")
            return False
        
        try:
            # Send the message
            self.sender_socket.sendall(message.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            # Try to reconnect once
            if self.connect_to_target(self.target_ip):
                try:
                    self.sender_socket.sendall(message.encode('utf-8'))
                    return True
                except Exception as e:
                    print(f"Failed to send even after reconnection: {e}")
            return False
    
    def close_chat(self):
        """Close the chat and all connections"""
        print("Closing chat application...")
        
        # Close the sender connection
        if self.sender_socket:
            self.sender_socket.close()
            self.sender_socket = None
            
        # Stop listening (which also closes client connections)
        self.listening = False
        self.connected = False
        
        # Close the client connection if active
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            
        # Close the listener socket
        if self.listener_socket:
            self.listener_socket.close()
            self.listener_socket = None
        
        print("Chat application closed")





if __name__ == "__main__":
    # Create chat application
    chat = ChatApplication()
    
    # Print local IP address for the user
    my_hostname = socket.gethostname()
    my_ip = socket.gethostbyname(my_hostname)
    print(f"Your IP address is: {my_ip}")
    
    # Start listening for messages
    chat.start_listening()
    
    # Get the target IP from the user
    target_ip = input("Enter the IP address of the other device: ")
    
    # Connect to the target
    if not chat.connect_to_target(target_ip):
        print("Failed to connect. The other device might not be listening yet.")
        print("Continuing anyway... You can try sending messages later.")
    
    # Simple chat loop
    try:
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break
                
            if chat.send_message(message):
                print(f"Sent: {message}")
            else:
                print("Failed to send message. The other device might not be connected.")
                # Ask if user wants to try connecting again
                retry = input("Try connecting again? (y/n): ")
                if retry.lower() == 'y':
                    new_ip = input("Enter the IP address to connect to (or press Enter to use the same): ")
                    if not new_ip:
                        new_ip = target_ip
                    chat.connect_to_target(new_ip)
                
    except KeyboardInterrupt:
        print("\nInterrupt received")
    finally:
        chat.close_chat()