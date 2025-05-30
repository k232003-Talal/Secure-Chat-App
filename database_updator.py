""" our public ips can change dynamically after a few days,
    OR if we use the account on a different device. 
    so we can use a database to keep track of/ update our ips """


import socket
import design
import firebase_admin
from firebase_admin import credentials, db

def get_machines_public_ip():
     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Google DNS (does not send actual data)
        return s.getsockname()[0]


cred = credentials.Certificate(design.database_json_file_path)            #REPLACE THIS WITH THE PATH TO YOUR CREDENTAILS CERTIFICATE (change in design.py)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://cn-project-f9b34-default-rtdb.firebaseio.com/'}) #REPLACE THIS WITH YOUR FIREBASE DATABASE URL


def download_from_firebase():
    ref = db.reference("user-info")
    data = ref.get()

    with open(design.data_file_path, "w") as file:
        file.write(data)  


def upload_to_firebase():
    with open(design.data_file_path, "r") as file:
        data = file.read()

    ref = db.reference("user-info") 
    ref.set(data)