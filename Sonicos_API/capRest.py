#-*-coding:utf-8-*-
import requests
import json
import urllib3
import pyotp
import os
urllib3.disable_warnings()

# Get current One-time Password




class capRest:

    def __init__(self, username, password):
        self.username = username
        self.password = password


    def getOTP(self,secretKey):
        totp = pyotp.TOTP(secretKey)
        cur_otp = totp.now()
        return cur_otp


	# Create a file to save token
    def base_dir(self):
        return os.path.join(os.path.dirname(__file__), 'token.md')


	# Read token
    def getToken(self):
        with open(self.base_dir(), 'r') as f:
            return f.read()		


    # Login
    def Login(self,ipstr,secretKey):
        cur_otp = self.getOTP(secretKey)
        url = 'https://' + ipstr + '/api/sonicos/tfa'
        body = {'user': self.username, 'password': self.password, 'tfa': cur_otp, 'override': True}
        headers = {'Accept': 'application/json', 'Accept-Encoding': 'application/json'}
        r = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
        res = str(r.content)
        token = res.split('BearToken: ')[-1].split('\"')[0]
        with open(self.base_dir(), 'w') as f:
            f.write(token)
        if (r.status_code == 200):
            print("Login successful." + "token:" + token)
        else:
            print ("status_code for login=" + str(r.status_code))
            print ("Login failed,please check session is valid.")
        return token

    # Logout
    def Logout(self,ipstr):
        url = 'https://' + ipstr + '/api/sonicos/auth'
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        r = requests.delete(url, headers=headers, verify=False)
        if (r.status_code == 200):
            print ("Logout successfully!")
        else:
            print ("status_code for logout=" + str(r.status_code))
            print ("Logout failed!")


    # Post data
    def post(self,ipstr,num):
        url = 'https://' + ipstr + '/api/sonicos/address-objects/ipv4'
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        for i in range(num):
            name = "test" + str(i)
            zone = "LAN"
            a = 1
            b = 1
            c = 1
            a += 1
            if a >= 255:
                a = 1
                b += 1
                if b >=255:
                    b = 1
                    c +=1
            host_ip = "18." +str(c)+ "."+str(b) + "." + str(a)
            body = {
                "address_objects": [
                    {
                        "ipv4": {
                            "name": name,
                            "zone": zone,
                            "host": {
                                "ip": host_ip
                            }
                        }
                    }
                ]
            }
            r = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
            if (r.status_code == 200):
                print ("Post " + str(i + 1) + " object successfully!")
            else:
                print ("status_code for post=" + str(r.status_code))
                print ("Post" + str(i + 1) + "object failed!please check session is valid or objects added is exist")

    # Commit configuration
    def commit(self,ipstr):
        url = 'https://' + ipstr + '/api/sonicos/config/pending'
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        r = requests.post(url, headers=headers, verify=False)
        if (r.status_code == 200):
            print ("Commit all pending configuration successfully!")
        else:
            print ("status_code for commit=" + str(r.status_code))
            print ("Commit failed,please check session is valid.")

            # Get the number of current objects

    def getAO(self,ipstr):
        url = 'https://' + ipstr + '/api/sonicos/address-objects/ipv4'
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        r = requests.get(url, headers=headers, verify=False)
        ss = r.json()
        list = ss["address_objects"]
        num = len(list)
        if (r.status_code == 200):
            print ("Current objects number=" + str(num))
        else:
            print ("status_code for get=" + str(r.status_code))
            print ("Get failed,please check session is valid.")
        return (num)


    def addAO(self,ipstr,num):
        url = 'https://' + ipstr + '/api/sonicos/address-objects/ipv4'
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        for i in range(num):
            name = "addr" + str(i)
            zone = "LAN"
            a = 1
            b = 1
            c = 1
            a += 1
            if a >= 255:
                a = 1
                b += 1
                if b >=255:
                    b = 1
                    c +=1
            host_ip = "18." +str(c)+ "."+str(b) + "." + str(a)
            body = {
                "address_objects": [
                    {
                        "ipv4": {
                            "name": name,
                            "zone": zone,
                            "host": {
                                "ip": host_ip
                            }
                        }
                    }
                ]
            }
            r = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
            if (r.status_code == 200):
                print ("Post " + str(i + 1) + " object successfully!")
            else:
                print ("status_code for post=" + str(r.status_code))
                print ("Post" + str(i + 1) + "object failed!please check session is valid or objects added is exist")
        url1 = 'https://' + ipstr + '/api/sonicos/config/pending'
        r1 = requests.post(url1, headers=headers, verify=False)
        if (r1.status_code == 200):
            print ("Commit all pending configuration successfully!")
        else:
            print ("status_code for commit=" + str(r1.status_code))
            print ("Commit failed,please check session is valid.")

    def delAO(self,ipstr,num):
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        for i in range(num):
            name = "addr" + str(i)
            url = 'https://' + ipstr + '/api/sonicos/address-objects/ipv4/name/' + name
            r = requests.delete(url, headers=headers, verify=False)
            if (r.status_code == 200):
                print ("Delete " + name + " successfully!")
            else:
                print ("status_code for delete=" + str(r.status_code))
                print ("delete " + name + " failed!")
        url1 = 'https://' + ipstr + '/api/sonicos/config/pending'
        r1 = requests.post(url1, headers=headers, verify=False)
        if (r1.status_code == 200):
            print ("Commit all pending configuration successfully!")
        else:
            print ("status_code for commit=" + str(r1.status_code))
            print ("Commit failed,please check session is valid.")

    def getSO(self,ipstr):
        url = 'https://' + ipstr + '/api/sonicos/service-objects'
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        r = requests.get(url, headers=headers, verify=False)
        ss = r.json()
        list = ss["service_objects"]
        num = len(list)
        if (r.status_code == 200):
            print ("Current objects number=" + str(num))
        else:
            print ("status_code for get=" + str(r.status_code))
            print ("Get failed,please check session is valid.")
        return (num)

    def addSO(self,ipstr,num):
        url = 'https://' + ipstr + '/api/sonicos/service-objects'
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        for i in range(num):
            name = "service"+str(i)
            body = body = {
                "service_objects": [
                    {
                        "ipv4": {
                            "name": name,
                            "tcp":{
                            	"begin":10,
                            	"end":10
                            }
                        }
                    }
                ]
            }
            r = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
            if (r.status_code == 200):
                print ("Post " + str(i + 1) + " object successfully!")
            else:
                print ("status_code for post=" + str(r.status_code))
                print ("Post" + str(i + 1) + "object failed!please check session is valid or objects added is exist")
        url1 = 'https://' + ipstr + '/api/sonicos/config/pending'
        r1 = requests.post(url1, headers=headers, verify=False)
        if (r1.status_code == 200):
            print ("Commit all pending configuration successfully!")
        else:
            print ("status_code for commit=" + str(r1.status_code))
            print ("Commit failed,please check session is valid.")

    def delSO(self,ipstr,num):
        headers = {'Authorization': 'Bearer ' + self.getToken(), 'Accept-Encoding': 'application/json'}
        for i in range(num):
            name = "service" + str(i)
            url = 'https://' + ipstr + '/api/sonicos/service-objects/name/' + name
            r = requests.delete(url, headers=headers, verify=False)
            if (r.status_code == 200):
                print ("Delete " + name + " successfully!")
            else:
                print ("status_code for delete=" + str(r.status_code))
                print ("delete " + name + " failed!")
        url1 = 'https://' + ipstr + '/api/sonicos/config/pending'
        r1 = requests.post(url1, headers=headers, verify=False)
        if (r1.status_code == 200):
            print ("Commit all pending configuration successfully!")
        else:
            print ("status_code for commit=" + str(r1.status_code))
            print ("Commit failed,please check session is valid.")
