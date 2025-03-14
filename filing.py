import os
import re

current_directory = os.path.dirname(__file__)  # Making sure the file is always created in the same folder with the program
file_path = os.path.join(current_directory, 'User_data.txt')
key_file_path= os.path.join(current_directory, 'key.txt')

def list_to_strings(Plain_Text):
  string_text=""
  for line in Plain_Text:
   string_text= string_text + line
  return string_text

def set_des_key():
   with open(key_file_path, 'r') as file:
    key_des = file.read()
    return  key_des
   

#-------------------------- Helper Functions Start ------------------------------------------

def des_decrypt_message(Private_key,key_des):
   return Private_key

def hash_Password(Plain_Text):
  hashed_password=Plain_Text
  return hashed_password

def get_file_data_string():
  try:
    with open(file_path, 'r') as userFile:
     string_data=userFile.read()
     string_data=string_data.split('\n')  #making an iteratable list wrt \n's

     i=0
     while (i < len(string_data)):
        string_data[i]=string_data[i] +'\n' #restoring the \n
        i=i+1

     return  string_data
  except FileNotFoundError:  
     return "File is Empty"

def get_txt_file_data():
  
  File_data=get_file_data_string()
  Data_to_display=""
  for line in File_data:
    Data_to_display= Data_to_display + line
  return Data_to_display


def get_All_Usernames(): #for signing up, Username must be unique, it cant already exist in file
  
  All_Usernames=[]
  File_data=get_file_data_string()

  for line in File_data:
     if("Username: " in line):
        Username=line.replace("Username: ", "").strip() #Extract Username
        All_Usernames.append(Username)
      
  return All_Usernames


def extract_proper_key(keystring):                     # function to slice string from (a,b) format to a and b. returns a list of integers
    match = re.match(r'\((\d+),\s*(\d+)\)', keystring)
    if match:
        part1 = int(match.group(1))
        part2 = int(match.group(2))
        key_pair=[part1,part2]
        return key_pair
    else:
        raise ValueError("String format is incorrect")

#-------------------------- Helper Functions END ---------------------------------------------



#-------------------------- Login Procedure Start ------------------------------------------- 
def Check_In_File(Input_data):
  Entered_Username = Input_data[0]
  Entered_Password = Input_data[1]
  Entered_Password=hash_Password(Entered_Password)
  This_Account_Id="0"


  Username_to_check = f'Username: {Entered_Username}\n'
  Password_to_check = f'Password: {Entered_Password}\n'

  File_data=get_file_data_string()
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
def get_IP(Acount_Id):

    File_data=get_file_data_string()
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Account ID:" in line and Acount_Id in line):
           line=File_data[i+3]
           IP_address=line.replace("Ip_address: ", "").strip() #Extract IP 
           break

        i=i+1
    return IP_address

def get_Username(Acount_Id):

    File_data=get_file_data_string()
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
    File_data=get_file_data_string()
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+5]
           Private_key=line.replace("Private Key: ", "").strip() #Extract Private Key (hashed)
           key_des=set_des_key()
           Private_key=des_decrypt_message(Private_key,key_des)
           Private_key=extract_proper_key(Private_key)
           return Private_key
        i=i+1
    return ""    

def get_Public_key(Username):
    
    Public_key=""
    File_data=get_file_data_string()
    i = 0
    while (i < len(File_data)):
        
        line = File_data[i]
        if("Username: " in line and Username in line):
           line=File_data[i+4]
           Public_key=line.replace("Public Key: ", "").strip() #Extract Public Key (hashed)
           key_des=set_des_key()
           Public_key=des_decrypt_message(Public_key,key_des)
           Public_key=extract_proper_key(Public_key)
           return Public_key
        i=i+1
    return ""   

#-------------------------- Extract  Keys Procedures Ends ---------------------------

def Update_Password(Username,new_password):
     new_password=hash_Password(new_password)
     File_data=get_file_data_string()
     i = 0
     while (i < len(File_data)):
        line = File_data[i]
        if("Username: " in line and Username in line):

            new_Password_string= f'Password: {new_password}\n'
            Update_Account_Data(i+1,new_Password_string,File_data)
            break
        i=i+1

def Update_IP_address(Username,new_IP_address):
     File_data=get_file_data_string()
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
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("Erroring deleting file in updation")
        
        with open(file_path, 'w') as file:
            for line in file_data:
              file.write(line)
            print("Account Data updated Successfully")  
    
      except Exception as e:
        print(f"An error occurred: {e}")


def check_old_password(Username,entered_password):
     File_data=get_file_data_string()
     i = 0
     while (i < len(File_data)):
        line = File_data[i]
        if("Username: " in line and Username in line):
            line=File_data[i+1]
            old_password=line.replace("Password: ", "").strip()
            entered_password=hash_Password(entered_password)
            if(entered_password==old_password):
                return 1
            else:
                return 0
        i=i+1  
     print("Error Fetching the password")
     return -1