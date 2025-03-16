import tkinter
import design
import time
import threading
import os
import msg_security
import filing


last_modified_time=None #represents the last time the chatlogs were modified, used to handle new messages being displyaed

# functions to show place holders in "send msg" field ------------------------------------------------------------------------

def on_focus_in(event, entry, placeholder_text):
    if entry.get("1.0", "end-1c") == placeholder_text:
        entry.delete("1.0", "end")  # Remove the placeholder text
        entry.config(fg="black")  # Change text color to black when typing

def on_focus_out(event, entry, placeholder_text):
    if entry.get("1.0", "end-1c") == "":
        entry.insert("1.0", placeholder_text)
        entry.config(fg="gray")  # Placeholder text color set back to gray  

#-------------------------------------------------------------------------------------------------------------------------------


#This will show red color for daniyal and Talal wherever they appear in the conversation
def highlight_Users(text_widget):
    words_to_highlight = ["Dani", "Talal"]

    for word in words_to_highlight:
        start = "1.0"
        while True:
            start = text_widget.search(word, start, stopindex=tkinter.END)
            if not start:
                break
            end = f"{start}+{len(word)}c" # start is the line, len(word)c means move n characters forward, where n is length of words
            text_widget.tag_add("highlight", start, end)
            start = end  # Move past the current match
    text_widget.tag_configure("highlight", foreground="red")

def go_back(window):
    window.withdraw() #hide the window
    window.after(1000, window.destroy) #wait for the loadtext_function to stop, destroy after 1 sec

#called if a new message is sent by either users, to reload the text on screen. 
def load_text(text_widget):
        
        global last_modified_time
        
        current_modified_time = os.stat(design.chat_logs_file_path).st_mtime        #if txt file has been modified, that means new msg has arrived.
        if last_modified_time is None or current_modified_time > last_modified_time:
            last_modified_time = current_modified_time
            
            txt_data=filing.get_txt_file_data(design.chat_logs_file_path)
        
            text_widget.config(state="normal")  #enabling writing in the text widget temporarily
            text_widget.delete("1.0", tkinter.END)  # Clear old text
            text_widget.insert(tkinter.END, txt_data)
            highlight_Users(text_widget) 
            text_widget.see(tkinter.END)
            text_widget.config(state="disabled") #this makes widget read only (so that user cant directly edit the widget on screen)

        chat_window = text_widget.winfo_toplevel()
        if chat_window.state() != "withdrawn":
           text_widget.after(1000, lambda: load_text(text_widget)) # call this function again every second to check for any new messages


def send_msg_to_other_user(msg,My_username):
    encrypted_msg=msg_security.RSA_encrypt(msg,My_username)
    #sockets function called here. 
    

def send_msg(msg,Username):
    filing.append_msg_chat(msg,Username)
    send_msg_to_other_user(msg,Username)        
    print("message Sent successfully")

def Start_Chat(Username):


    """ 
    replace the line below with the ACTUAL thread that recieves msg

    logic: The line below works with the temporary 'recv_msg_from_other_user' function. simulates how the chat function will run concurrently with recieve msg function. It is not part of the final logic

        -) the recieve function simulates new msgs by constantly appending "lmaooooo" or ":y'dddddd" (depending on why you login as) to the chat every 8 seconds
          
        -)   the loadtext function in the 'start_chat' function runs every second to check any new msgs

        -)  if new msg found, the chat updates on screen.

        -)  if you send a msg, that also updates on screen.

    """

    threading.Thread(target=recv_msg_from_other_user,args=([2350, 3637, 1137, 2098, 2098, 2098, 2098, 2098],Username,), daemon=True).start()  #daemon=True makes threads stop when program halts

    Chat_window = tkinter.Tk()
    Chat_window.title("End to End Ecrypted Chat") 

    #  the calculation below is To centre the window that appears on the screen
    screen_width = Chat_window.winfo_screenwidth()       
    screen_height = Chat_window.winfo_screenheight()     
    window_width = 1160                                  
    window_height = 760                                        
    X_cord = (screen_width // 2) - (window_width // 2)   
    Y_cord = (screen_height // 2) - (window_height // 2)  
    Chat_window.geometry(f"{window_width}x{window_height}+{X_cord}+{Y_cord}") 

    Chat_window.config(bg="black")
    Msg_placeholder="your message.."
    Chat_frame=tkinter.LabelFrame(Chat_window) 
    Chat_frame.grid(row=0,column=0 ,padx=20,pady=10)

    text_widget = tkinter.Text(Chat_frame, wrap="word",width=90, font=design.Entry_label_font, fg="black")
    text_widget.grid(row=0,column=0, pady=10, ipady=5,sticky="w")
    
    highlight_Users(text_widget)

    scrollbar = tkinter.Scrollbar(Chat_frame, command=text_widget.yview)
    scrollbar.grid(row=0,column=1, ipadx=7, sticky="ns")      #sticky="ns" is streching scrollbar vertically
    load_text(text_widget)
    text_widget.config(yscrollcommand=scrollbar.set) 

    msg_entry=tkinter.Text(Chat_frame,font=design.Entry_label_font, bg="white",fg="gray", width=90,height=5, wrap="word")
    msg_entry.insert("1.0", Msg_placeholder)
    msg_entry.grid(row=1,column=0,pady=10, ipady=5,sticky="w")

    msg_entry.bind("<FocusIn>", lambda event: on_focus_in(event, msg_entry, Msg_placeholder))
    msg_entry.bind("<FocusOut>", lambda event: on_focus_out(event, msg_entry, Msg_placeholder))

    def send_button_function():
        Entered_msg =msg_entry.get("1.0", "end-1c")
        if(Entered_msg==Msg_placeholder or Entered_msg ==""):
            return
        elif(len(Entered_msg)>500):
            print(("Msg too big to send."))
            return
        else:
            send_msg(Entered_msg,Username)
            msg_entry.delete("1.0", "end")

    button_frame=tkinter.Frame(Chat_frame) 
    button_frame.grid(row=1,column=1 ,padx=20,pady=10) 

    Send_button = tkinter.Button(button_frame, bg="black" , text="Send" ,command=send_button_function, **design.Button_style_4,**design.Simple_Button_style)
    Send_button.grid(row=1,column=0,padx=10,pady=(20,10))

    Close_button = tkinter.Button(button_frame, bg="red" , text="Close" ,command=lambda: go_back(Chat_window), **design.Button_style_4,**design.Simple_Button_style)
    Close_button.grid(row=2,column=0,padx=10,pady=(20,10))

    Chat_window.mainloop()

""" temporary function to demonstrate new messages """

def recv_msg_from_other_user(msg,My_username):
    while True:
        time.sleep(8)
        decrypted_msg=msg_security.RSA_decrypt(msg,My_username)
        other_user=filing.get_other_Username(My_username)
        filing.append_msg_chat(decrypted_msg,other_user)

# Start_Chat("Talal")      
