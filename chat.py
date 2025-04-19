import tkinter
import design
import os
import msg_security
import filing
import sockcli

last_modified_time = None

def on_focus_in(event, entry, placeholder_text):
    if entry.get("1.0", "end-1c") == placeholder_text:
        entry.delete("1.0", "end")
        entry.config(fg="black")

def on_focus_out(event, entry, placeholder_text):
    if entry.get("1.0", "end-1c") == "":
        entry.insert("1.0", placeholder_text)
        entry.config(fg="gray")

def highlight_Users(text_widget,My_Username):
    other_username= filing.get_other_Username(My_Username)
    words_to_highlight = [My_Username,other_username]

    for word in words_to_highlight:
        start = "1.0"
        while True:
            start = text_widget.search(word, start, stopindex=tkinter.END)
            if not start:
                break
            end = f"{start}+{len(word)}c"
            text_widget.tag_add("highlight", start, end)
            start = end
    text_widget.tag_configure("highlight", foreground="red")

def go_back(window):
    for widget in window.winfo_children():
        if isinstance(widget, tkinter.Text) and hasattr(widget, "after_id"):
            widget.after_cancel(widget.after_id)
    window.withdraw()
    try:
       window.after(1000, lambda: window.destroy() if window.winfo_exists() else None)
    except:
        pass    #window already destroyed   
    
    """ the load_text function below employs periodic updates to the chat window through the after() method of tkinter. This method schedules a callback function
        to be executed after a delay (1000 milliseconds in this case). Each time the callback is triggered, load_text() checks if the chat log file has been modified
        by comparing its last modified timestamp with a stored value (last_modified_time). If changes are detected, it reloads the chat data from the file, updates the chat widget,
        and highlights relevant usernames. This cycle continues as long as the chat window is open, with the next update scheduled after 1 second, ensuring that the chat window 
        stays up-to-date with new messages without manually refreshing. """

def load_text(text_widget,my_username,first_time=False):
    global last_modified_time

#if its the first time calling this function. load text without relying on the scheduller. this ensure that if chat is closed and opened again. msgs are displayed without the need to modify the file first.

    if first_time==True: 
        first_time=False
        txt_data = filing.get_txt_file_data(design.chat_logs_file_path)
        text_widget.config(state="normal")
        text_widget.delete("1.0", tkinter.END)
        text_widget.insert(tkinter.END, txt_data)
        highlight_Users(text_widget,my_username)
        text_widget.see(tkinter.END)
        text_widget.config(state="disabled")

#if file modified. only then update the chat

    current_modified_time = os.stat(design.chat_logs_file_path).st_mtime
    if last_modified_time is None or current_modified_time > last_modified_time:
        last_modified_time = current_modified_time
        txt_data = filing.get_txt_file_data(design.chat_logs_file_path)
        text_widget.config(state="normal")
        text_widget.delete("1.0", tkinter.END)
        text_widget.insert(tkinter.END, txt_data)
        highlight_Users(text_widget,my_username)
        text_widget.see(tkinter.END)
        text_widget.config(state="disabled")

    try:
        # Cancel any previous scheduled call first
        if hasattr(text_widget, "after_id"):
            text_widget.after_cancel(text_widget.after_id)
    except Exception:
        pass

    try:
        # Store the ID of the new scheduled call
        text_widget.after_id = text_widget.after(1000, lambda: load_text(text_widget, my_username))
    except Exception:
        pass


def send_msg_to_other_user(chat_obj, msg, My_username):
    encrypted_msg = msg_security.RSA_encrypt(msg, My_username)
    chat_obj.send_message(encrypted_msg)

def send_msg(chat_obj, msg, Username):
    filing.append_msg_chat(msg, Username)
    send_msg_to_other_user(chat_obj, msg, Username)
    print("message Sent successfully")

def Start_Chat(Username):
    Chat_window = tkinter.Tk()
    Chat_window.title("End to End Encrypted Chat")

    screen_width = Chat_window.winfo_screenwidth()
    screen_height = Chat_window.winfo_screenheight()
    window_width = 1160
    window_height = 760
    X_cord = (screen_width // 2) - (window_width // 2)
    Y_cord = (screen_height // 2) - (window_height // 2)
    Chat_window.geometry(f"{window_width}x{window_height}+{X_cord}+{Y_cord}")
    Chat_window.config(bg="black")

    Msg_placeholder = "your message.."
    Chat_frame = tkinter.LabelFrame(Chat_window)
    Chat_frame.grid(row=0, column=0, padx=20, pady=10)

    text_widget = tkinter.Text(Chat_frame, wrap="word", width=90, font=design.Entry_label_font, fg="black")
    text_widget.grid(row=0, column=0, pady=10, ipady=5, sticky="w")
    highlight_Users(text_widget,Username)

    scrollbar = tkinter.Scrollbar(Chat_frame, command=text_widget.yview)
    scrollbar.grid(row=0, column=1, ipadx=7, sticky="ns")
    load_text(text_widget,Username,first_time=True)
    text_widget.config(yscrollcommand=scrollbar.set)

    msg_entry = tkinter.Text(Chat_frame, font=design.Entry_label_font, bg="white", fg="gray", width=90, height=5, wrap="word")
    msg_entry.insert("1.0", Msg_placeholder)
    msg_entry.grid(row=1, column=0, pady=10, ipady=5, sticky="w")

    msg_entry.bind("<FocusIn>", lambda event: on_focus_in(event, msg_entry, Msg_placeholder))
    msg_entry.bind("<FocusOut>", lambda event: on_focus_out(event, msg_entry, Msg_placeholder))

    def send_button_function():
        Entered_msg = msg_entry.get("1.0", "end-1c")
        if Entered_msg == Msg_placeholder or Entered_msg == "":
            return
        elif len(Entered_msg) > 500:
            print("Msg too big to send.")
            return
        else:
            send_msg(chat_socket_obj, Entered_msg, Username)
            msg_entry.delete("1.0", "end")

    button_frame = tkinter.Frame(Chat_frame)
    button_frame.grid(row=1, column=1, padx=20, pady=10)

    Send_button = tkinter.Button(button_frame, bg="black", text="Send", command=send_button_function,
                                 **design.Button_style_4, **design.Simple_Button_style)
    Send_button.grid(row=1, column=0, padx=10, pady=(20, 10))

    def close_chat():
        try:
            chat_socket_obj.send_message("__CLOSE__")
        except:
            pass
        go_back(Chat_window)

    Close_button = tkinter.Button(button_frame, bg="red", text="Close", command=close_chat,
                                  **design.Button_style_4, **design.Simple_Button_style)
    Close_button.grid(row=2, column=0, padx=10, pady=(20, 10))

    chat_socket_obj = sockcli.start_chat_sockets(Username, Chat_window)

    """The chat_obj returned by the sockcli.start_chat_sockets() function is an instance of the ChatApplication class, which is responsible for managing the connection,
      sending and receiving messages. It handles socket connections using self.listener_socket for listening and self.sender_socket for sending messages. 
      The ChatApplication object manages the connection to the target user by calling methods like connect_to_target() and send_message() to securely transmit data,
        and it uses the message_queue for asynchronous message handling via a separate thread (sending_thread)."""
    
    Chat_window.protocol("WM_DELETE_WINDOW", close_chat) #if the red cross button on the top right is clicked, behave the same way as when the custom  clase button is clicked

    Chat_window.mainloop()
