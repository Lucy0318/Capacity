#-*-coding:utf-8-*-
import requests
import json
import pyotp
import os
import urllib3
import time

urllib3.disable_warnings()

#Get current One-time Password
def getOTP(secretKey):
    totp = pyotp.TOTP(secretKey)
    cur_otp = totp.now()
    return cur_otp


#Create a file to save token
def base_dir():
    return os.path.join(os.path.dirname(__file__), 'token.md')


#Read token
def getToken():
    with open(base_dir(),'r') as f:
        return f.read()

#Login
def login(ipstr,secretKey):
    cur_otp=getOTP(secretKey)
    url = 'https://' + ipstr + '/api/sonicos/tfa'
    body = {'user': 'admin', 'password': 'password', 'tfa': cur_otp, 'override': True}
    headers = {'Accept': 'application/json', 'Accept-Encoding': 'application/json'}
    r = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
    res = str(r.content)
    token = res.split('BearToken: ')[-1].split('\"')[0]
    with open(base_dir(), 'w') as f:
        f.write(token)
    if (r.status_code == 200):
        print("Login successful."+"token:"+token)
    else:
        print ("status_code for login=" + str(r.status_code))
        print ("Login failed,please check session is valid.")
    return token


#Get the number of current objects
def get(ipstr):
    url = 'https://' + ipstr + '/api/sonicos/address-objects/ipv4'
    header = {'Authorization': 'Bearer ' + getToken(), 'Accept-Encoding': 'application/json'}
    r = requests.get(url, headers=header, verify=False)
    ss=r.json()
    list = ss["address_objects"]
    num = len(list)
    if (r.status_code == 200):
        print ("Current objects number="+str(num))
    else:
        print ("status_code for get="+str(r.status_code))
        print ("Get failed,please check session is valid.")
    return (num)


#Post data
def post(ipstr,num):
    url = 'https://'+ipstr+'/api/sonicos/address-objects/ipv4'
    headers = {'Authorization': 'Bearer ' + getToken(), 'Accept-Encoding': 'application/json'}
    a = 1
    b = 1
    c = 1
    value_list = []
    for i in range(num):
        name1="test"+str(i)
        zone1="LAN"
        if a >= 255:
            a = 1
            b += 1
            if b >= 255:
                b = 1
                c += 1
        host_ip1 = "19." + str(c) + "." + str(b) + "." + str(a)
        dic1={}
        dic={"ipv4":dic1}
        named=name1
        zoned=zone1
        hostd={"ip":host_ip1}
        dic1["name"]=named
        dic1["zone"]=zoned
        dic1["host"]=hostd
        value_list.append(dic)
        a += 1
    body = {"address_objects": value_list}
    print(type(body))
    print(body)
    print(type(value_list))
    data=json.dumps(body)
    print(type(data))
    print(data)
        # data=str(body)
    r = requests.post(url, data=data, headers=headers, verify=False)
    # r = requests.post(url, data=body, headers=headers, verify=False)
    if (r.status_code == 200):
        print ("Post "+str(num)+ " object successfully!")
    else:
         print ("status_code for post="+str(r.status_code))
         print ("Post"+str(num)+ "object failed!please check session is valid or objects added is exist")




#Commit configuration
def commit(ipstr):
    url = 'https://'+ ipstr +'/api/sonicos/config/pending'
    headers = {'Authorization': 'Bearer ' + getToken(), 'Accept-Encoding': 'application/json'}
    r = requests.post(url, headers=headers, verify=False)
    print ("status_code for commit=" + str(r.status_code))
    if (r.status_code == 200):
        print ("Commit all pending configuration successfully!")
    else:
        print ("Commit failed,please check session is valid.")



def delete(ipstr,num):
    for i in range(num):
        name="test"+str(i)
        url = 'https://' + ipstr + '/api/sonicos/address-objects/ipv4/'+ name
        headers = {'Authorization': 'Bearer ' + getToken(), 'Accept-Encoding': 'application/json'}
        r = requests.delete(url, headers=headers, verify=False)
        if (r.status_code == 200):
            print ("Delete " + name+" successfully!")
        else:
            print ("status_code for delete=" + str(r.status_code))
            print ("delete "+name+ " failed!")


#Logout
def logout(ipstr):
    url = 'https://' + ipstr + '/api/sonicos/auth'
    headers = {'Authorization': 'Bearer ' + getToken(), 'Accept-Encoding': 'application/json'}
    r = requests.delete(url, headers=headers, verify=False)
    if (r.status_code == 200):
        print ("Logout successfully!")
    else:
        print ("status_code for logout=" + str(r.status_code))
        print ("logout failed!")


if __name__ == '__main__':
    secretKey = "H6FY2FHO4OBBULLVZ7UIEHW3LI"
    ipstr = '10.7.3.96'
    num=2
    #login and get current address objects
    login(ipstr,secretKey)
    get(ipstr)
    #add num address objects and verify whether post successfully
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    post(ipstr,num)
    commit(ipstr)
    get(ipstr)
    #delete all additons and check the remain objects
    delete(ipstr,num)
    commit(ipstr)
    get(ipstr)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # logout
    logout(ipstr)