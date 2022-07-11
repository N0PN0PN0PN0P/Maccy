# menu
# random, scelta per produttore oppure imputalo manualmente secondo l hex
# clone an airodump mac

# LIB IMPORTS
import os
import subprocess as sp
import optparse
import re
import requests
from bs4 import BeautifulSoup
import random as rnd
import asyncio


# CLASS TO IMPLEMENT COLORING LINES IN TERMINAL
class Bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# GLOBAL VARS
macs_in_file = []
hex_converter = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
cwd = os.getcwd()
macs_file_name = "mac_addresses.txt"
parser = optparse.OptionParser()
parser.add_option("-d", "--debug", action="store_true", help="Enter in debug mode")
(options, arguments) = parser.parse_args()
debug = options.debug


# THIS BLOCK DOES AN API REQUEST TO THE WEBSITE https://api.macaddress.io TO POST THE OUI MAC
# AND RETRIEVE THE VENDOR ID
# PLEASE REGISTER TO https://api.macaddress.io TO OBTAIN YOUR API QUERY KEY TO GET THE NAME OF THE MAC PRODUCER(OUI
async def getMacProducer(oui):
    api_key_macaddress_io = "at_1lsy9vcEFSDX4z8pCBMFRFKxJND3z"
    macaddress_io_url_request = "https://api.macaddress.io/v1?apiKey=" + api_key_macaddress_io + "&output=vendor&search=" + oui
    response = requests.get(macaddress_io_url_request)
    if debug:
        debby(str(response.text))
    await asyncio.sleep(1)
    return response.text


# CREATE A REAL MAC ADDRESS STARTING FROM THO VENDOR'S OUI (OEM ORGANIZATIONALLY UNIQUE IDENTIFIER)
def createRandomMac():
    rnd.seed()
    print(Bcol.OKCYAN + "[+] Creating the REAL MAC address..." + Bcol.ENDC)
    rnd_producer = rnd.sample(macs_in_file, 1)
    rnd_hex_num = rnd.sample(hex_converter, 6)
    temp_mac = (rnd_producer + rnd_hex_num)
    temp_mac = ''.join(temp_mac)
    final_mac = ':'.join(temp_mac[i:i + 2] for i in range(0, len(temp_mac), 2))
    print(Bcol.OKGREEN + "[+] Getting name of the MAC address producer..." + Bcol.ENDC)
    macProducer = asyncio.run(getMacProducer(str(final_mac)))
    if debug == True:
        debby(str(macProducer) + " : " + str(final_mac))
    print(Bcol.OKGREEN + "[+] MAC address producer: " + Bcol.FAIL + macProducer + Bcol.ENDC)
    return final_mac


# THIS BLOCK INITIALIZE THE PROGRAM, AT FIRST RUN CHECKS IF THE FILE CONTAINING THE MAC ADDRESSES EXIST,
# IF IT DOES THE PROGRAM LOADS THE 20000 OUI MAC ADDRESSES IN THE MAC'S LIST TO BE USED LATER.
# IF THE FILE DOESN'T EXIST IT USES BEAUTYFUL SOUP TO SCRAPE 25 PAGES ON https://www.netlookup.se/mac/vendors/
# AND GETS ABOUT 20000 MAC'S OUI AND SAVE IN THE FILE AND IN THE MAC'S LIST TO BE USED LATER ON
def initialize():
    pagecount = 1
    totalpages = 25
    if debug == True:
        debby(cwd)
    try:
        if debug == True:
            debby("Open file that contains prescraped real MACs")
        print(Bcol.WARNING + "[+] Opening file to import REAL MAC addresses." + Bcol.ENDC)
        f = open(cwd + "/" + macs_file_name, "r")
        print(Bcol.WARNING + "[+] Populating the array with REAL MAC addresses." + Bcol.ENDC)
        for macs in f:
            # if debug == True:
            #   debby(macs)
            macs_in_file.append(macs.strip("\n"))
            # if debug == True:
            #   print(macs_in_file)
    except FileNotFoundError as e:
        try:
            f = open(cwd + "/" + macs_file_name, "w")
            if debug == True:
                debby(e)
            print(Bcol.FAIL + "[!] Can't Open the file mac_addresses.txt, file doesn't exist!" + Bcol.ENDC)
            # CREATE THE FILE TO HOLD THE SCRAPER MAC ADDRESSES
            print(Bcol.OKCYAN + "[+] Start Scraping the website for REAL MAC addresses." + Bcol.ENDC)
            print(Bcol.WARNING + "[+] Total pages to scrape: " + str(totalpages) + Bcol.ENDC)

            while pagecount < totalpages + 1:
                print(Bcol.WARNING + "[+] Scraping page: " + str(pagecount) + Bcol.ENDC)
                URL = "https://www.netlookup.se/mac/vendors/?page=" + str(pagecount)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                producersMacs = soup.find_all("td", class_="d-none d-lg-block")
                for producerMac in producersMacs:
                    if debug == True:
                        print(producerMac.getText(separator="\n", strip=True))
                    temp_str = str(producerMac.getText(separator="\n", strip=True))
                    if debug == True:
                        debby("Len of items: " + str(len(temp_str)))
                    if len(temp_str) < 7:
                        f.write(temp_str + "\n")
                        macs_in_file.append(temp_str)
                pagecount += 1
            print(Bcol.OKCYAN + "[+] Total REAL MAC addresses added: " + str(len(macs_in_file)) + Bcol.ENDC)
            f.close()
            if debug == True:
                print(macs_in_file)
        except Exception as e:
            print(e)

# WELL TAHNK YOU GUYS :P
def thankyou():
    asterisk()
    print("\r")
    print(Bcol.OKCYAN + "[*] THANK YOU FOR USING MACCY ;) : " + Bcol.ENDC)
    print(Bcol.OKCYAN + "[*] please send any comments to N0PN0PN0P@proton.me ;) : " + Bcol.ENDC)
    print("\r")
    asterisk()

# DEBBY IS THE PRINTOUT DEBUGGER YOU CAN USE FROM THE TERMINAL WITH -d AFTER THE PROGRAM NAME
def debby(debug_string):
    print(Bcol.FAIL + "\n[Debug]: " + str(debug_string) + Bcol.ENDC)
    # print("\r")

# WELL ASTERIX AND OBELIX :P ... I DON'T LIKE PARSERS
def asterisk():
    print(Bcol.OKCYAN + "*" * 100 + Bcol.ENDC)

# BEAUTIFUL ASCII ART I LOVE IT
def show_menu():
    # Menu Build
    sp.call("clear", shell=True)
    asterisk()
    print("███    ███  █████   ██████  ██████ ██    ██")
    print("████  ████ ██   ██ ██      ██       ██  ██")
    print("██ ████ ██ ███████ ██      ██        ████")
    print("██  ██  ██ ██   ██ ██      ██         ██")
    print("██      ██ ██   ██  ██████  ██████    ██")
    asterisk()
    print(Bcol.HEADER + "OP MAC address changer by N0PN0PN0P")
    print("Mail: N0PN0PN0P@proton.me")
    print("Github : https://github.com/N0PN0PN0PN0P/maccy")
    print("Favourite quote : 'I don't like PARSERS'")
    print(
        "With my api key you can do only 100 free queries per day,\nso please sign in to https://macaddress.io to get your free api key" + Bcol.ENDC)
    asterisk()

# THIS BLOCK CHECKS FOR ROOT PRIVS BECAUSE YOU NEED THEM TO CHANGE THE MAC ADDRESS
def check_root_priv():
    print("[+] Remember to run the program as sudo: change the MAC address require sudoers privileges")
    print("[+] Checking if you have root permissions...")
    isRoot = sp.check_output("id -u", shell=True)
    if debug == True:
        debby("Checking Uid: " + str(isRoot))
    isRoot = isRoot.decode("utf-8").strip()
    if debug == True:
        debby("Decoding Utf-8 the Uid: " + str(isRoot))
    if isRoot != "0":
        print(
            Bcol.FAIL + "[!] You are not running the program as sudoer (root), please type: sudo maccy.py" + Bcol.ENDC)
        exit(1)
    else:
        print(Bcol.WARNING + "[+] " + "You have root permissions moving on..." + Bcol.ENDC)

# THIS BLOCK ENUMERATES AND RETRIEVES ALL THE MAC INTERFACES IN YOUR SYSTEM, IT DOESN'T RETRIEVE THE LOOPBACK (LP)
def get_interfaces():
    print('[+] These are the available interfaces in your system:')
    availInterfaces = sp.check_output("ip link | awk -F: '$0 !~ \"lo|vir|^[^0-9]\"{print $2;getline}' 2>/dev/null ",
                                      shell=True)
    if debug == True:
        debby("Getting available interfaces: " + str(availInterfaces))
    availInterfaces = availInterfaces.decode("utf-8")
    if debug == True:
        debby("Decoding available interfaces: " + str(availInterfaces))
    netInterfaces = []
    for lan in availInterfaces.split("\n"):
        netInterfaces.append(lan.strip())
        if debug == True:
            debby("Append " + lan + " in the netInterfaces Array.")
    if debug == True:
        debby("Strip empty entries in netInterfaces array")
    netInterfaces = list(filter(str.strip, netInterfaces))
    i = 0
    for choice in netInterfaces:
        print(Bcol.HEADER + "[+] " + str(i) + ") :  " + choice + Bcol.ENDC)
        i += 1
    return netInterfaces

# THIS BLOCK USES LINUX SHELL COMMAND IP + GREP + AWK ( LOVE IT ) TO RETRIEVE AND STORE THE MAC OF THE PASSED INTERFACE
def getMacaddress(selected_interface):
    mac = sp.check_output(
        "ip link show " + selected_interface + " | grep link/ether | awk '{print $2}' 2>/dev/null ",
        shell=True).decode("utf-8").strip()
    if debug == True:
        debby(Bcol.FAIL + "getMacaddress function : Previous MAC address " + mac + Bcol.ENDC)
    return mac

# THIS BLOCK USES LINUX SHELL COMMAND IFCONFIG AND REGEX ( REGULAR EXPRESSIONS ) TO RETRIEVE AND STORE THE MAC
# OF THE PASSED INTERFACE
def getMacaddressRegex(selected_interface):
    ifconfig_result = sp.check_output(["ifconfig", selected_interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        if debug == True:
            debby(Bcol.FAIL + "getMacaddressRegex function : Previous MAC address " + mac_address_search_result.group(
                0) + Bcol.ENDC)
        return str(mac_address_search_result)
    else:
        print(Bcol.WARNING + "[!] Can't find a valid MAC address for: " + selected_interface + Bcol.ENDC)
        return 0

# THE CORE OF THE CODE HERE WE REALLY CHANGE THE MAC ADDRESS OF THE SELECTED INTERFACE AND CHECK IF IT IS
# CORRECTLY CHANGED
def setMacaddress(mac_tochange, interface, previous_mac):
    print(Bcol.WARNING + "[+] Setting NEW MAC address..." + Bcol.ENDC)
    if debug == True:
        debby("New Mac: " + mac_tochange + " - Interface: " + interface + " - Previous Mac: " + previous_mac)
    print(Bcol.WARNING + "[+] Shutting OFF: " + Bcol.FAIL + interface + Bcol.ENDC + ".")
    sp.check_output(["ifconfig", interface, "down"])
    print(
        Bcol.WARNING + "[+] Setting " + Bcol.FAIL + interface + " MAC address to " + Bcol.FAIL + mac_tochange + Bcol.ENDC + ".")
    sp.check_output(["ifconfig", interface, "hw", "ether", mac_tochange])
    print(Bcol.WARNING + "[+] Turnin ON: " + Bcol.FAIL + interface + Bcol.ENDC + ".\n")
    sp.check_output(["ifconfig", interface, "up"])
    check_mac = getMacaddress(interface)
    if check_mac != previous_mac:
        print(
            Bcol.OKCYAN + "[!] " + interface + " MAC address successfully changed : Old MAC: " + previous_mac + " - New MAC: " + check_mac + "\n" + Bcol.ENDC)
    else:
        print(Bcol.FAIL + "[!] COULD NOT CHANGE THE MAC PLEASE REPORT TO GITHUB.\n")



# BLOCK TO DEFINE THE MAIN ACTION OF THE PROGRAM: CHANGE THE MAC ADDRESS
def change_MAC(choice):
    if choice == 1:
        # USING REGEX TO VALIDATE THE USER MAC INPUT
        mac_to = ""
        print((Bcol.OKCYAN + "[!] Please remember to use hex notation, every 2 chars add a :(colon)" + Bcol.ENDC))
        print((Bcol.OKGREEN + "[+] Valid entries are: " + Bcol.FAIL + ','.join(hex_converter) + Bcol.ENDC))
        while not re.match(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",mac_to):
            mac_to = input(Bcol.WARNING + "[!] Please input a valid MAC address: > " + Bcol.ENDC)
        setMacaddress(mac_to, selected_interface, previous_mac_address)
    if choice == 2:
        realMac = createRandomMac()
        print(Bcol.OKGREEN + "[+] This will be your new MAC address: " + Bcol.FAIL + realMac + Bcol.ENDC)
        keep_mac = "N"
        while keep_mac != "Y" and keep_mac != "G":
            keep_mac = input(Bcol.OKCYAN + "[?] Are you " + Bcol.FAIL +
                             "Ok" + Bcol.OKCYAN + " with this or you want to " +
                             Bcol.FAIL + "Generate " + Bcol.OKCYAN + "a new one? (" + Bcol.FAIL + "Y" +
                             Bcol.OKCYAN + "/" + Bcol.FAIL + "G" + Bcol.OKCYAN + ") " + Bcol.ENDC).upper()
        if keep_mac == "Y":
            setMacaddress(realMac, selected_interface, previous_mac_address)
        else:
            change_MAC(2)
    if choice == 3:
        return



# PROGRAM START
if debug == True:
    debby("Parser Options: " + str(parser.parse_args()))

show_menu()
initialize()
check_root_priv()
netInterfaces = get_interfaces()
intAmount = len(netInterfaces)
adapterch = 10000000

# LOOP TO LET THE USER INPUT THE INTERFACE TO CHANGE THE MAC
while adapterch > len(netInterfaces) - 1 or adapterch < 0:
    try:
        adapterch = int(input(
            Bcol.WARNING + "[?] Please type the number of the interface you want to change the MAC address: > " + Bcol.ENDC))
        if adapterch > len(netInterfaces) - 1 or adapterch < 0:
            print(Bcol.FAIL + "[!] Please input the correct interface number!" + Bcol.ENDC)
    except ValueError:
        print(Bcol.FAIL + "[!] Please input a number!" + Bcol.ENDC)
print("\r")
asterisk()
print(Bcol.FAIL + "\n[!]" + Bcol.OKGREEN + " You selected interface " + Bcol.FAIL + netInterfaces[
    adapterch] + Bcol.ENDC + ", current MAC address: " +
      Bcol.FAIL + sp.check_output(
    "ip link show " + netInterfaces[adapterch] + " | grep link/ether | awk '{print $2}' 2>/dev/null ",
    shell=True).decode("utf-8").strip() +
      Bcol.ENDC)
# ASSIGNING RETRIEVED VALUES
selected_interface = str(netInterfaces[adapterch])
previous_mac_address = str(getMacaddress(selected_interface))
previous_mac_address_regex = str(getMacaddressRegex(selected_interface))
print("\r")
# ip link show eth0 | grep link/ether | awk '{print $2}'
asterisk()
print(Bcol.WARNING + "\n[+] Choose an option: " + Bcol.ENDC)
print("[+] 1) Input a MAC address.")
print("[+] 2) Impersonate a real device ( use real MAC addresses from real producers ).")
print("[+] 3) Exit program.")
macchoice = 5
while macchoice > 4 or macchoice < 1:
    try:
        macchoice = int(input(Bcol.WARNING + "[?] Please input your choice number: > " + Bcol.ENDC))
        if macchoice > 4 or macchoice < 1:
            print(Bcol.FAIL + "[!] Please input a number included between 1 and 4!" + Bcol.ENDC)
    except ValueError:
        print(Bcol.FAIL + "[!] Please input a number!" + Bcol.ENDC)

change_MAC(int(macchoice))
thankyou()
exit(0)
