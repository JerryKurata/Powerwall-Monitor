#
#    Powerwall-monitor.py
#
#   This script monitors a powerwall by polling the PW interface.
#   The information gathered can be written to a file and evaluated for various condition 
#   if the condition exists, a handler for the condition is invoked
#
#   Work is based on this great repo of the Powerwall Gateway API
#       https://github.com/vloschiavo/powerwall2
#

#   Import libraries
import sys
import argparse
import json
import urllib3   # used to prevent display of Unverified HTTPS request warning
from datetime import datetime
from powerwall_comm import gateway  # methods to communication with PW Gateway

#   Constants
#gw_url = "https://powerwall"    # powerwall = ip address is in my hosts file  # replacable with command line arg 
#gw_cert_path = "cacert.pem"

# To do: test and add more methods!

#   Acquisition - gets data from all sources
#       get data from Powerwall Gateway
#       get data from Inverters

def dump_json(title, json_output):
    print(title, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print( json.dumps(json_output, indent=4))

# Entry point of main acquisition
def main(gw_addr, gw_cert_path):
    print('in main')

    gw_url = "https://" + gw_addr
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # disabled this warning 
    gw = gateway(gw_url, gw_cert_path)

    print()
    state_of_charge_json = gw.getMeterStateOfCharge().json()
    dump_json("State of charge (json formatted)",state_of_charge_json)
    
    # Site name
    dump_json("Site name (json formatted)", gw.getSiteName().json())
    meter_power_output = gw.getMeterPower()
    # print("Meter Power (raw):",meter_power_output)
    meter_power_json = meter_power_output.json()
    dump_json("Meter Power (json formatted)",meter_power_json)
    # meter_power_parsed = json.loads(meter_power_json)
    print("Site:", meter_power_json['site'])
    print ("Key - value pairs for Site")
    for k, v in meter_power_json['site'].items():
        print ("    ", k, v)

    meter_soc_json = gw.getMeterStateOfCharge().json()
    dump_json("Meter state of charge (json formatted)", meter_soc_json)
    for k, v in meter_soc_json.items():
        print ("    ", k, v)
    # print("Meter Power (json):", json_output)
    # print("Meter Power (json formatted):")
    # print( json.dumps(json_output, indent=4))


# if running as main (i.e. from command line)
if __name__ == "__main__":

    # parse command line arguments
    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser()
  
    # default of 'powerwall' reference entry in HOSTS file containing ip addr of gateway
    # default to carcert.pem as name of certificate user created (NOT CURRENLY USED)
    ap.add_argument('--gw_address',  default="powerwall", help="name or address of powerwall gateway" )
    ap.add_argument('--gw_cert',  default="cacert.pem", help="path to certification file" )
 
    # An illustration of how access the arguments.
    args = ap.parse_args()

    # print("gw_address:", args.gw_address)
    # print("gw_cert:", args.gw_cert)
  
    main(args.gw_address, args.gw_cert)


