import json
import requests
import time
import os

ticket_url = "http://localhost:58000/api/v1/ticket"

print("Network Programibility: Local LMS Network")
#username = input("Username: ")
#password = input("Password: ")

headers = {
    "content-type": "application/json"
}

body_json = {
   # "username": username,
   # "password": password  
   "username": "1sAdmin",
   "password": "1sAdm1nPass!" 
}

respon = requests.post(ticket_url, json.dumps(body_json), headers=headers, verify=False)
respon_json = respon.json()
if respon.status_code > 201 :
    print("Login Fail/Error,",respon_json["response"]["message"])
    exit()

print("Login Success")
serviceTicket = respon_json["response"]["serviceTicket"]
aksi = 99

headers={"X-Auth-Token": serviceTicket}

while aksi != 0:
    os.system('clear')
    print("Pilih Aksi:")
    print("1. Network Devices List")
    print("2. Host List")
    print("3. Network Issue")
    print("4. Network Health")
    print("0. Quit")
    aksi = int(input("Masukan Nomor Aksi: "))
    if aksi == 0:
        break
    elif aksi == 1:
        os.system('clear')
        url = "http://localhost:58000/api/v1/network-device"

        respon = requests.get(url, headers=headers, verify=False)

        print("Network Devices List ")

        respon_json = respon.json()
        networkDevices = respon_json["response"]

        print("Hostname\tType\tIP")
        for networkDevice in networkDevices:
            print(networkDevice["hostname"], "\t", networkDevice["platformId"], "\t", networkDevice["managementIpAddress"])
        d = input("\npress Enter to Back")
        continue
    elif aksi == 2:
        os.system('clear')
        url = "http://localhost:58000/api/v1/host"

        respon = requests.get(url, headers=headers, verify=False)

        print("Host List ")

        respon_json = respon.json()
        hosts = respon_json["response"]

        print("Hostname\tIP\tMac Address\tConnected Interface")
        for host in hosts:
            print(host["hostName"], "\t", host["hostIp"], "\t", host["hostMac"], "\t", host["connectedInterfaceName"])
        d = input("\npress Enter to Back")
        continue
    elif aksi == 3:
        os.system('clear')
        url = "http://localhost:58000/api/v1/assurance/health-issues"

        respon = requests.get(url, headers=headers, verify=False)

        print("Health Issues")

        respon_json = respon.json()
        issues = respon_json["response"]

        print("Source\tIssue\tDescription\tTime")
        for issue in issues:
            print(issue["issueSource"], "\t", issue["issueName"], "\t", issue["issueDescription"], "\t", issue["issueTimestamp"])
        d = input("\npress Enter to Back")
        continue
    elif aksi == 4:
        os.system('clear')
        url = "http://localhost:58000/api/v1/network-health"

        respon = requests.get(url, headers=headers, verify=False)

        print("Network Health")

        health = respon.json()

        print(health)
        print("Clients Health: ",health["healthyClient"],"%")
        print("Network Devices Health: ",health["healthyNetworkDevice"],"%")
        print("Num Routers: ",health["numLicensedRouters"])
        print("Num Switches: ",health["numLicensedSwitches"])
        print("Num Unreachable: ",health["numUnreachable"])

        d = input("\npress Enter to Back")
        continue

headers = {
    "X-Auth-Token": serviceTicket
}
logout_url = "http://localhost:58000/api/v1/ticket/"+serviceTicket
r = requests.delete(logout_url, headers=headers, verify=False)
print(r.status_code)
print("Program Dihentikan")
