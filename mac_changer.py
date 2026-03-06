#usage python3 -i eth

import optparse
import re
import subprocess
#take 2 args, interface and mac address want to change
def get_arguments():
    
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='interface change its MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='New mac address')
    (options, args) = parser.parse_args()
    #check if args is valid
    if not options.interface:
        parser.error('[-] Please specify the interface you want to change its MAC address')
    elif not options.new_mac:
        parser.error('[-] Please specify the new mac address')
    return options
#shut down interface in order to change mac
def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address to {interface} to new MAC address: {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether",new_mac])
    subprocess.call(["ifconfig", interface, "up"])
#use subprocess lib call if config to find current mac, using re module.
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])

    mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search:
        return mac_address_search.group(0)
    else:
        print ("[-] Mac address not found")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f"[+] Current MAC address: {current_mac}")

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
#check if mac has changed or not
if current_mac == current_mac:
    print("[+] Current MAC address is the changed")
else:
    print("[-] Current MAC address is not changed")

