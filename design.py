#this file contains declarations of design and utilites variables/function


import os
#styles ---------------------------------------------------------------------------------------------------------------------------------------------

X_cord=600   #these represent where to show GUI window on screen
Y_cord=130

Main_Heading_font= ("Chiller", 45, "bold")
Sub_Headings_font= ("Arial Black", 17, "bold")
Other_Headings_font= ("Arial Black", 30, "bold")
Simple_text_font= ("Arial", 15, "bold")
Button_font1=("Arial Black", 20, "bold")
Button_font2=("Arial Black", 15, "bold")
Entry_label_font=("Arial", 15)
Data_Display_font=("Arial", 10,"bold")
Other_labels_font=("Arial", 15, "bold")

Basic_Button_style = {
    "fg": "white",
    "relief": "raised",
    "borderwidth": 10,
    "activebackground":"white",  # Hover background color
    "activeforeground":"black"  # Hover text color
}

Button_style_1 = {
    "font": Button_font1,
    "width": 10,
    "height": 1,
}

Button_style_2 = {
    "font": Button_font2,
    "width": 10,
    "height": 2,
}

Button_style_3 = {
    "font": Button_font2,
    "width": 20,
    "height": 2,
}
#styles END ---------------------------------------------------------------------------------------------------------------------------------------------


#OS configuration ---------------------------------------------------------------------------------------------------------------------------------------

current_directory = os.path.dirname(__file__)  # Making sure the file is always created in the same folder with the program
file_path = os.path.join(current_directory, 'User_data.txt')
key_file_path= os.path.join(current_directory, 'key.txt')

def remove_file(path):
   os.remove(path)

def already_exists(path):
 return os.path.exists(path)


#OS configuration END ------------------------------------------------------------------------------------------------------------------------------------


#AUXILARY FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------

#this function makes sure the errors are wrapped with the frame, and dont overflow
def Wrap_over_newline(mystring, limit=20): 
    words = mystring.split() 
    current_length = 0
    result = []
    for word in words:
        # If adding this word would exceed the limit, insert a newline
        if current_length + len(word) > limit:
            result.append('\n')
            current_length = 0 
        result.append(word) 
        current_length += len(word) + 1  # accounting the space after the word

    return ' '.join(result)  #rejoin with spaces

def list_to_strings(Plain_Text):
  string_text=""
  for line in Plain_Text:
   string_text= string_text + line
  return string_text

#AUXILARY FUNCTIONS END --------------------------------------------------------------------------------------------------------------------------------------

