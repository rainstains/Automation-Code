import json
import requests
import time
import os

def sendingTheMessage(message):
    PostData = {
                "roomId": roomId,
                "text": message
               }
    r = requests.post( "https://webexapis.com/v1/messages", 
                            data = json.dumps(PostData), 
                            headers = webex_Headers
                     )

def networkHealth(webex = False):
    url = "http://localhost:58000/api/v1/network-health"

    r = requests.get(url, headers=headers, verify=False)
    health = r.json()

    if webex == False:
        print("Network Health")
        print("Clients Health: ",health["healthyClient"],"%")
        print("Network Devices Health: ",health["healthyNetworkDevice"],"%")
        print("Num Routers: ",health["numLicensedRouters"])
        print("Num Switches: ",health["numLicensedSwitches"])
        print("Num Unreachable: ",health["numUnreachable"])
        next= input("\npress Enter to Back")
    elif webex == True:
        message = "Clients Health: "+health["healthyClient"]+"%"+"\n"
        message += "Network Devices Health: "+health["healthyNetworkDevice"]+"%"+"\n"
        message += "Num Routers: "+health["numLicensedRouters"]+"\n"
        message += "Num Switches: "+health["numLicensedSwitches"]+"\n"
        message += "Num Unreachable: "+health["numUnreachable"]+"\n"
        sendingTheMessage(message)

def networkIssues(webex = False):
    url = "http://localhost:58000/api/v1/assurance/health-issues"

    r = requests.get(url, headers=headers, verify=False)
    r_json = r.json()
    issues = r_json["response"]

    if webex == False:
        print("Health Issues")
        print("Source\tIssue\tDescription\tTime")
        for issue in issues:
            print(issue["issueSource"], "\t", issue["issueName"], "\t", issue["issueDescription"], "\t", issue["issueTimestamp"])
        next= input("\npress Enter to Back")
    elif webex == True:
        message = "Source\tIssue\tDescription\tTime\n"
        for issue in issues:
            message += issue["issueSource"]+ "\t"+ issue["issueName"]+ "\t"+ issue["issueDescription"]+ "\t"+ issue["issueTimestamp"]+ "\n"
        sendingTheMessage(message)

def hostList(webex = False):
    url = "http://localhost:58000/api/v1/host"

    r = requests.get(url, headers=headers, verify=False)
    r_json = r.json()
    hosts = r_json["response"]

    if webex == False:
        print("Host List ")
        print("Hostname\tIP\tMac Address\tConnected Interface")
        for host in hosts:
            print(host["hostName"], "\t", host["hostIp"], "\t", host["hostMac"], "\t", host["connectedInterfaceName"])
        next= input("\npress Enter to Back")
    elif webex == True:
        message = "Hostname\tIP\tMac Address\tConnectenextInterface\n"
        for host in hosts:
            message += host["hostName"]+ "\t"+ host["hostIp"]+ "\t"+ host["hostMac"]+ "\t"+ host["connectedInterfaceName"]+ "\n"
        sendingTheMessage(message)

def deviceList(webex = False):
    url = "http://localhost:58000/api/v1/network-device"

    r = requests.get(url, headers=headers, verify=False)
    r_json = r.json()
    networkDevices = r_json["response"]

    if webex == False:
        print("Network Devices List ")
        print("Hostname\tType\tIP")
        for networkDevice in networkDevices:
            print(networkDevice["hostname"], "\t", networkDevice["platformId"], "\t", networkDevice["managementIpAddress"])
        next= input("\npress Enter to Back")
    elif webex == True:
        message = "Hostname\tType\tIP\n"
        for networkDevice in networkDevices:
            message += networkDevice["hostname"]+ "\t"+ networkDevice["platformId"]+ "\t"+ networkDevice["managementIpAddress"]+ "\n"
        sendingTheMessage(message)

def listeningToWebex():
    print("Listening To Webex Messages ...")
    while True:
        time.sleep(5)
        GetParameters = {
                                "roomId": roomId,
                                "max": 1
                        }
        r = requests.get("https://webexapis.com/v1/messages", 
                            params = GetParameters, 
                            headers = {"Authorization": accessToken}
                        )
        if not r.status_code == 200:
            raise Exception( "Incorrect reply from Webex Teams API. Status code: {}. Text: {}".format(r.status_code, r.text))
        
        json_data = r.json()
        if len(json_data["items"]) == 0:
            raise Exception("There are no messages in the room.")
        
        messages = json_data["items"]
        message = messages[0]["text"]
        print("Received message: " + message)
        
        if message == "/Network Device List":
            deviceList(webex = True)
        elif message == ("/Host List"):
            hostList(webex = True)
        elif message == ("/Network Issues"):
            networkIssues(webex = True)
        elif message == ("/Network Health"):
            networkHealth(webex = True)
        elif message == ("/Terminate"):
            break

#Program utama dimulai
ticket_url = "http://localhost:58000/api/v1/ticket"
accessToken = "Bearer MWJjYWY4MmUtNjFkYS00MDIwLTlhNzktY2Q3MGNiZjBkZmIzNTgxNmZhMDQtNWYz_P0A1_1abaf078-5b80-48ca-9bb3-46107517275f"
roomId = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vZjYxOWU4MDAtZmFhYS0xMWVjLWIxMWItMWYwZWIzY2YwMWE4"
webex_Headers = { 
                    "Authorization": accessToken,
                    "Content-Type": "application/json"
                }


print("Network Programibility Using Rest API")
print("Network: Local LMS Network in SMK 4")
username = input("Username: ")
password = input("Password: ")

headers = {
    "content-type": "application/json"
}

body_json = {
   "username": username,
   "password": password  
}

r = requests.post(ticket_url, json.dumps(body_json), headers=headers, verify=False)
r_json = r.json()
if r.status_code > 201 :
    print(r_json["response"]["message"])
    responseMessage = "Someone attempt to login using username: "+username+" From Python Code and Failed! ("+time.ctime()+")"
    sendingTheMessage(responseMessage)
    exit()

print("Login Success")
print("Welcome ", username)
responseMessage = "User: "+username+" has Successfully Login From Python Code! ("+time.ctime()+")"
sendingTheMessage(responseMessage)
serviceTicket = r_json["response"]["serviceTicket"]
action = 76

headers={"X-Auth-Token": serviceTicket}
next= input("\npress Enter to Back")
while action != 0:
    os.system('clear')
    print("Action List")
    print("1. Network Devices List")
    print("2. Host List")
    print("3. Network Issues")
    print("4. Network Health")
    print("5. Listening To Webex Room")
    print("0. Exit")
    action = int(input("Enter Number Action: "))
    if action == 0:
        break
    elif action == 1:
        os.system('clear')
        deviceList()
        continue
    elif action == 2:
        os.system('clear')
        hostList()
        continue
    elif action == 3:
        os.system('clear')
        networkIssues()
        continue
    elif action == 4:
        os.system('clear')
        networkHealth()
        continue
    elif action == 5:
        os.system('clear')
        listeningToWebex()
        continue

# API untuk Delete Tidak Bisa digunakan
#logout_url = "http://localhost:58000/api/v1/ticket/"+serviceTicket
#r = requests.delete(logout_url, headers=headers)
print("Program Terminated")
print("Network Automation: Code v1.4")