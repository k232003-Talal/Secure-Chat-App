#our public ips can change dynamically after a few days, OR if we use the account on a different device

#pip install requests
# pip install firebase-admin
import requests
import design
import firebase_admin
from firebase_admin import credentials, db

def get_machines_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    if response.status_code == 200:
        ip = response.json()['ip']
        return ip
    else:
        return None

#Connecting the script to firebase database
cred = credentials.Certificate(design.database_json_file_path) 
firebase_admin.initialize_app(cred, {'databaseURL': 'https://cn-project-f9b34-default-rtdb.firebaseio.com/'})


def download_from_firebase():
    ref = db.reference("user-info")
    data = ref.get()

    with open(design.data_file_path, "w") as file:
        file.write(data)  


def upload_to_firebase():
    with open(design.data_file_path, "r") as file:
        data = file.read()

    ref = db.reference("user-info")  # Change to Firestore method if using Firestore
    ref.set(data)
    print("Database Updated")

# upload_to_firebase()
# download_from_firebase()
# ip = get_machines_public_ip()
# print("public IP address:",ip)