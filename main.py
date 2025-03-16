import tkinter
import time
import design
import chat
from filing import *
from ip_updator import get_machines_public_ip

def go_back(this_window):
    this_window.destroy()

def Log_out(Account_Window):
    Account_Window.destroy()
    Login_Function()     


    """ 
        Read the message in the Chat.py before running. 
        the password for both, Talal and Dani is test1234 
    """

#PASSWORD ----------------------------------------------------------------------------------------------------

def Change_Password(This_username):
    Change_Password_window = tkinter.Tk()
    Change_Password_window.title("Change Password") 
    Change_Password_window.geometry(f"610x590+{design.X_cord}+{design.Y_cord}") 
    Change_Password_window.config(bg="black")

    ID_label=tkinter.Label(Change_Password_window,font=design.Other_Headings_font, bg="black", fg="#D8a616" ,text="Change Password") 
    ID_label.grid(row=0,column=0,pady=(20,30))

    Change_password_frame=tkinter.LabelFrame(Change_Password_window) 
    Change_password_frame.grid(row=1,column=0 ,padx=20,pady=10)

    Button_Frame=tkinter.LabelFrame(Change_Password_window,bg="black",  relief="flat") 
    Button_Frame.grid(row=5,column=0 ,padx=20,pady=10)

    Old_password_label=tkinter.Label(Change_password_frame,font=design.Other_labels_font,text="Old Password")   #(this is one of the contained labels)
    Old_password_label.grid(row=1,column=0, pady=10, ipady=5)

    Old_password_entry=tkinter.Entry(Change_password_frame,font=design.Entry_label_font, bg="white",fg="gray", width=35,show="*")
    Old_password_entry.grid(row=1,column=1, padx=10, pady=10, ipady=5,ipadx=5)

    New_Password=tkinter.Label(Change_password_frame,font=design.Other_labels_font,text="New Password")
    New_Password.grid(row=2,column=0, pady=10, ipady=5)

    New_Password_entry=tkinter.Entry(Change_password_frame,font=design.Entry_label_font, bg="white",fg="gray", width=35,show="*")
    New_Password_entry.grid(row=2,column=1, padx=10, pady=10, ipady=5)

    Confirm_New_Password=tkinter.Label(Change_password_frame,font=design.Other_labels_font,text="Confirm\nNew Password")
    Confirm_New_Password.grid(row=3,column=0, pady=10, ipady=5)

    Confirm_New_Password_entry=tkinter.Entry(Change_password_frame,font=design.Entry_label_font, bg="white",fg="gray", width=35,show="*")
    Confirm_New_Password_entry.grid(row=3,column=1, padx=10, pady=10, ipady=5)


    Error_label=tkinter.Label(Change_password_frame,font=design.Simple_text_font, fg="Red",justify="left",text="")  
    Error_label.grid(row=4,column=0, columnspan=2,pady=(10,20))  

    back_button = tkinter.Button(Button_Frame, bg="#901111", text="Cancel",command=lambda: go_back(Change_Password_window),**design.Button_style_2,**design.Basic_Button_style)
    back_button.grid(row=5,column=0, padx=20, pady=(20,10)) 

    def Submit_Change_Passwod_data():
        Entered_data = [
            Old_password_entry.get(),  
            New_Password_entry.get(),
            Confirm_New_Password_entry.get(), 
        ]
        error_text=Validate_Passwod_data(Entered_data,This_username)
        Error_label.config(text=error_text)   #if there is an error, display it
        if(error_text=="" or error_text==None):
            Change_Password_window.destroy()
            print("Password Change Successful")
            Update_Password(This_username,Entered_data[1]) 

    Submit_Data_button = tkinter.Button(Button_Frame, bg="#13780a" , text="Submit\nData",command=Submit_Change_Passwod_data, **design.Button_style_2,**design.Basic_Button_style)
    Submit_Data_button.grid(row=5,column=1,padx=20,pady=(20,10)) 

#------------------------------------------- Change_Password Functions END -------------------------------------------


def Validate_login_data(login_data):
    Account_Id=Check_In_File(login_data)      #function found in filing_logic.py it returns an id if account is found in file, otherwise returns "0"
    Result=[None,0]   #if account is found, we need the id, else we need to print an error, index 0 is error, index 1 is id
    if(Account_Id=="0"):
       Result[0]="Username or Password Is incorrect."
    else:   
        Result[1]=int(Account_Id)
     
    return Result

def Validate_Passwod_data(Entered_data,This_username):
    Old_Password,entered_password,entered_confirm_password=Entered_data

    def Validade_new_Password():
        Validation_error=None
        if(entered_password=="" or Old_Password=="" or entered_confirm_password==""):
            Validation_error="Password Fill all input fields." 
        elif(len(entered_password)<8):
            Validation_error="Password should be atleast 8 characters long." 
        if(len(entered_password)<8):
            Validation_error="Password should be atleast 8 characters long." 
        elif(entered_password!=entered_confirm_password):
            Validation_error="Password and Confirm Password fields do not match."
        elif(entered_password==Old_Password):
            Validation_error="New Password can not be the same as old password."
        elif(len(entered_password)>20):
            Validation_error="Password should be atmost 20 characters long."
        elif any(character in entered_password for character in ['#', '"', '\'','\n','!',':']):
            Validation_error="Password contains invalid characters."
        return Validation_error 

    NewPasswordError= Validade_new_Password()
    if(NewPasswordError == None):
       Old_Password_check=check_old_password(This_username,Old_Password)
       if(Old_Password_check!=1):
           return "Invalid Password."
       
    elif(NewPasswordError != None):
        return NewPasswordError

    else:
        return ""


# Functions to remove or Add Placeholder text --------------------------------------------------
def on_focus_in(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tkinter.END)  # Remove the placeholder text
        entry.config(fg="black")  # Change text color to black when typing
        if(placeholder_text=="Password" or placeholder_text=="Confirm Password"):
            entry.config(show="*")  #if user is entering a password, show * instead of actual letters


def on_focus_out(event, entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")  # Placeholder text color set back to gray
        if(placeholder_text=="Password" or placeholder_text=="Confirm Password"):
            entry.config(show="") # (in case of password) when nothing in field, show the placeholder instead of '*' 
#----------------------------------------------------------------------------------------------------

# #USER ACC --------------------------------------------------------------------------------------------------------


def Show_User_Account(Acount_Id):
    # Creating the main window
    User_Account_Window = tkinter.Tk()
    User_Account_Window.title("User Account")
    User_Account_Window.geometry(f"465x475+{design.X_cord}+{design.Y_cord}")  
    User_Account_Window.config(bg="black")

    Username=get_Username(Acount_Id)


#User_Account Label
    ID_label=tkinter.Label(User_Account_Window,font=design.Main_Heading_font, bg="black", fg="white" ,text=Username) 
    ID_label.grid(row=0,column=0,pady=(15,15))

    user_frame=tkinter.LabelFrame(User_Account_Window,bg="black",  relief="flat") #relief="flat" sets visible boderwidth to 0
    user_frame.grid(row=1,column=0 ,padx=20,pady=10)

    Chat_button = tkinter.Button(user_frame, bg="#15aacb" , text="Chat",command=lambda: chat.Start_Chat(Username), **design.Button_style_2,**design.Basic_Button_style)
    Chat_button.grid(row=1,column=0,padx=25,pady=(20,10)) 


    Update_IP_button = tkinter.Button(user_frame, bg="#13780a" , text="Update\nIP",command=lambda: Update_IP(Username), **design.Button_style_2,**design.Basic_Button_style)
    Update_IP_button.grid(row=1,column=1,padx=20,pady=(20,10)) 

    Change_Password_button = tkinter.Button(user_frame, bg="#D8a616" , text="Change\nPassword",command=lambda: Change_Password(Username), **design.Button_style_2,**design.Basic_Button_style)
    Change_Password_button.grid(row=2,column=0,padx=20,pady=(20,10)) 

    Log_out_button = tkinter.Button(user_frame, bg="#901111", text="Log out",command=lambda: Log_out(User_Account_Window),**design.Button_style_2,**design.Basic_Button_style)
    Log_out_button.grid(row=2,column=1,padx=20,pady=(20,10)) 

    def Update_IP(This_username):
        updated_IP=get_machines_public_ip()
        if(updated_IP is None):
             print("unable to fetch Ip")
        else:     
             Update_IP_button.config(bg="#ffffff")  # Change color to white
             Update_IP_address(This_username,updated_IP)
             time.sleep(1) 
             print("Ip updated Successfully")
             Update_IP_button.config(bg="#13780a")  # Change back after 1 second


#LOGIN ---------------------------------------------------------------------------

def Login_Function():
   
   login_Window = tkinter.Tk()
   login_Window.title("Login Window")  # Title forlogin_Window
   login_Window.geometry(f"465x420+{design.X_cord}+{design.Y_cord}")  # Size forlogin_Window
   login_Window.config(bg="black")  # Set background color oflogin_Window
   
   name_placeholder = "Username"
   password_placeholder = "Password"

   Welcomelabel=tkinter.Label(login_Window,font=design.Other_Headings_font, bg="black", fg="Red" ,text="Login") 
   Welcomelabel.grid(pady=(10,10))
   
   login_frame=tkinter.LabelFrame(login_Window)
   login_frame.grid(row=1,column=0 ,padx=20,pady=(10,20))

   name_entry=tkinter.Entry(login_frame,font=design.Entry_label_font, bg="white",fg="gray", width=35)
   name_entry.grid(row=1,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   name_entry.insert(0, name_placeholder)

   Password_entry=tkinter.Entry(login_frame,font=design.Entry_label_font, bg="white",fg="gray", width=35)
   Password_entry.grid(row=2,column=0, padx=10, pady=10, ipady=5,ipadx=5)
   Password_entry.insert(0, password_placeholder)

   #when the user clicks on the submit button, this field becomes visible and displays errors (if any)
   Error_label=tkinter.Label(login_frame,font=design.Simple_text_font, fg="Red", justify="left",text="")  
   Error_label.grid(row=3,column=0,pady=(10,10))    

   def submit_login_data():  #nested functiion to get field values and display possible errors
      
        login_data = [
            name_entry.get(),  
            Password_entry.get(),  
        ]

        Acount_Id=0
        Validation_result = Validate_login_data(login_data)  #index 0 is error, index 1 is id
        error_text=""
        if(Validation_result[0] is not None):
            error_text=Validation_result[0] 
        else:
            Acount_Id=Validation_result[1]
        
        if(error_text!=""):                    #if there is an error, display it
           Error_label.config(text=error_text)
        else:
            login_Window.destroy()
            Show_User_Account(int(Acount_Id))

   Submit_button = tkinter.Button(login_frame, bg="green" , text="Login",command=submit_login_data,**design.Button_style_2,**design.Basic_Button_style)
   Submit_button.grid(row=4,column=0,padx=(0,20),pady=(20,20)) 


   name_entry.bind("<FocusIn>", lambda event: on_focus_in(event, name_entry, name_placeholder))
   name_entry.bind("<FocusOut>", lambda event: on_focus_out(event, name_entry, name_placeholder))

   Password_entry.bind("<FocusIn>", lambda event: on_focus_in(event, Password_entry, password_placeholder))
   Password_entry.bind("<FocusOut>", lambda event: on_focus_out(event, Password_entry, password_placeholder))

   login_Window.mainloop()
# -----------------------------------------------------------------------------------------------------------------------------------


Login_Function()