#our public ips can change dynamically after a few days, OR if we use the account on a different device

#pip install requests
import requests

def get_machines_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    if response.status_code == 200:
        ip = response.json()['ip']
        return ip
    else:
        return None




if __name__ == "__main__":
    ip = get_machines_public_ip()
    print("public IP address:",ip)