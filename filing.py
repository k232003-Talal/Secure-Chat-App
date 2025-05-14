import re
import design
import msg_security
import database_updator

#-------------------------- Helper Functions Start ------------------------------------------

#to avoid any errors while decrypting if user had entered a non printable character
def exclude_not_printable(text): 
    return ''.join(character for character in text if character.isprintable() or character == '\n')



#returns a list with each line as a seperate index
def get_file_data_string(path):
  
  string_data=None
  try:
    with open(path, 'r') as userFile:
     file_data=userFile.read()
     if(path==design.chat_logs_file_path):  #chats are encrypted with DES, other files are not.
         readable_data=msg_security.decrypt_message(file_data)
         readable_data=exclude_not_printable(readable_data)
         string_data=readable_data.split('\n')  #making an iteratable list wrt \n's
     else:  
         string_data=file_data.split('\n')

     i=0
     while (i < len(string_data)):
        string_data[i]=string_data[i] +'\n' #restoring the \n
        i=i+1

     return  string_data
  except FileNotFoundError:  
     return "File is Empty"

#returns entire data in the same format its stored in file
def get_txt_file_data(path):               
  
  File_data=get_file_data_string(path)
  Data_to_display=""
  for line in File_data:
    Data_to_display= Data_to_display + line
  return Data_to_display


def get_other_Username(my_Username): #for signing up, Username must be unique, it cant already exist in file
  
  All_Usernames=[]
  File_data=get_file_data_string(design.data_file_path)

  for line in File_data:
     if("Username: " in line):
        Username=line.replace("Username: ", "").strip() #Extract Username
        All_Usernames.append(Username)

  if(my_Username==All_Usernames[0]):    #for now we are working with only 2 users
        return All_Usernames[1]
  else:
        return All_Usernames[0]


#-------------------------- Helper Functions END ---------------------------------------------



#-------------------------- Login Procedure Start ------------------------------------------- 
def Check_In_File(Input_data):
  Entered_Username = Input_data[0]
  Entered_Password = Input_data[1]
  Entered_Password=msg_security.hash_data(Entered_Password)
  This_Account_Id="0"


  Username_to_check = f'Username: {Entered_Username}\n'
  Password_to_check = f'Password: {Entered_Password}\n'

  File_data=get_file_data_string(design.data_file_path)
  i = 0
  while (i < len(File_data)):
        
        line = File_data[i]
      
        if "Account ID:" in line:
            This_Account_Id = line.split("Account ID: ")[1].strip().split()[0] #get this account ID to return if match found
            line= File_data[i+1]   #Line now contains username

        if(Username_to_check == line):

          this_password = File_data[i+2]   # get password of this user
          if(Password_to_check == this_password):
            print('Login Successful')
            return This_Account_Id
        i=i+1  

  return "0"
#-------------------------- Login Procedure ENDS -------------------------------------------


#-------------------------- Get Account Details Procedure STARTS ---------------------------


def get_Username(Acount_Id):

    File_data=get_file_data_string(design.data_file_path)
    i = 0
    while (i < len(File_data)):
        line = File_data[i]
        if("Account ID:" in line and str(Acount_Id) in line):
           line=File_data[i+1]
           Username=line.replace("Username: ", "").strip() #Extract Username
           break

        i=i+1
    return Username

#-------------------------- Get Account Details Procedure ENDS ---------------------------


#-------------------------- Extract Keys and QR file path Procedures Start ---------------------------

def get_Private_key(Username):
    
    Private_key=""
    File_data=get_file_data_string(design.data_file_path)
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+4]
           Private_key=line.replace("Private Key: ", "").strip() #Extract Private Key (hashed)
           Private_key=msg_security.decrypt_message(Private_key)
           Private_key=extract_proper_key(Private_key)
           return Private_key
        i=i+1
    return ""    

def get_User_ip(Username):
    
    user_ip=""
    File_data=get_file_data_string(design.data_file_path)
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+2]
           user_ip=line.replace("IP_address: ", "").strip() #Extract ip
           return user_ip
        i=i+1
    return "" 

def get_Public_key(Username):
    
    Public_key=""
    File_data=get_file_data_string(design.data_file_path)
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+3]
           Public_key=line.replace("Public Key: ", "").strip() #Extract Public Key (hashed)
           Public_key=msg_security.decrypt_message(Public_key)
           Public_key=extract_proper_key(Public_key)
           return Public_key
        i=i+1
    return ""   

def extract_proper_key(keystring):                     # function to slice string from (a,b) format to a and b. returns a list of integers
    match = re.match(r'\((\d+),\s*(\d+)\)', keystring)
    if match:
        part1 = int(match.group(1))
        part2 = int(match.group(2))
        key_pair=[part1,part2]
        return key_pair
    else:
        raise ValueError("String format is incorrect")

#-------------------------- Extract  Keys Procedures Ends ---------------------------

def Update_Password(Username,new_password):
     new_password=msg_security.hash_data(new_password)
     File_data=get_file_data_string(design.data_file_path)
     i = 0
     while (i < len(File_data)):
        line = File_data[i]
        if("Username: " in line and Username in line):

            new_Password_string= f'Password: {new_password}\n'
            Update_Account_Data(i+1,new_Password_string,File_data)
            break
        i=i+1

def Update_IP_address(Username,new_IP_address):
     database_updator.download_from_firebase()  #first get the data from firebase,
     File_data=get_file_data_string(design.data_file_path)
     i = 0
     while (i < len(File_data)):
        line = File_data[i]
        if("Username: " in line and Username in line):

            new_IP_address_string= f'IP_address: {new_IP_address}\n'
            Update_Account_Data(i+2,new_IP_address_string,File_data)
            break
        i=i+1        



def Update_Account_Data(line_number,new_data,file_data):
      file_data[line_number]=new_data
      try:
        if design.already_exists(design.data_file_path):
            design.remove_file(design.data_file_path)
        else:
            print("Error updating User data")
        
        with open(design.data_file_path, 'w') as file:
            for line in file_data:
              file.write(line)
    
      except Exception as e:
        print(f"An error occurred: {e}")

      database_updator.upload_to_firebase()      #upload your data to the databse so it can be accessed later.   


def check_old_password(Username,entered_password):
     File_data=get_file_data_string(design.data_file_path)
     i = 0
     while (i < len(File_data)):
        line = File_data[i]
        if("Username: " in line and Username in line):
            line=File_data[i+1]
            old_password=line.replace("Password: ", "").strip()
            entered_password=msg_security.hash_data(entered_password)
            if(entered_password==old_password):
                return 1
            else:
                return 0
        i=i+1  
     print("Error Fetching the password")
     return -1

def append_msg_chat(msg,Username):
    formated_msg=f"\n{Username}: {msg}\n"
    des_enc_msg=msg_security.encrypt_message(formated_msg)
    with open(design.chat_logs_file_path, "a") as file:
        file.write(des_enc_msg)