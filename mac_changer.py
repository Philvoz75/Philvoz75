import optparse
import re
import subprocess

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='interface change its MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='New mac address')
    (options, args) = parser.parse_args()

    if not options.interface:
        parser.error('[-] Please specify the interface you want to change its MAC address')
    elif not options.new_mac:
        parser.error('[-] Please specify the new mac address')
    return options
def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address to {interface} to new MAC address: {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ehter",new_mac])
    subprocess.call(["ifconfig", interface, "up"])

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
if current_mac == current_mac:
    print("[+] Current MAC address is the changed")
else:
    print("[-] Current MAC address is not changed")

