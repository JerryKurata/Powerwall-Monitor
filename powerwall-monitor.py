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
import time 
from datetime import datetime
from gateway_comm import gateway  # methods to communication with PW Gateway
from powerwall_db import db


#   Constants
dbHost = "localhost" # address of dbServer
dbDatabase = "powerwall"      # name of database 
dbUser = "powerwall_user"          # Username to authenticate
dbPassword = "PW_Admin1999"      # password to authenticate

#gw_url = "https://powerwall"    # powerwall = ip address is in my hosts file  # replacable with command line arg 
#gw_cert_path = "cacert.pem"


#trace_on = True     # set to true enable printing trace messages

# To do: test and add more methods!

#   Acquisition - gets data from all sources
#       get data from Powerwall Gateway
#       get data from Inverters



def display_json(title, json_output):
    print(title, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print( json.dumps(json_output, indent=4))

#   test harness
def test(gw_addr, gw_cert_path):
    print('in main')

    gw_url = "https://" + gw_addr
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # disabled this warning 
    gw = gateway(gw_url, gw_cert_path)

    print()
    # State of charge
    display_json("State of charge (json formatted)",gw.getMeterStateOfCharge().json())
    
    # Site name
    display_json("Site name (json formatted)", gw.getSiteName().json())

    # Power Walls
    display_json("Powerwalls (json formatted)", gw.getPowerwalls().json())

    # Meter Power
    meter_power_output = gw.getMeterPower()
    # print("Meter Power (raw):",meter_power_output)
    meter_power_json = meter_power_output.json()
    display_json("Meter Power (json formatted)",meter_power_json)
    # meter_power_parsed = json.loads(meter_power_json)
    # print("Site:", meter_power_json['site'])
    # print ("Key - value pairs for Site")
    # for k, v in meter_power_json['site'].items():
    #     print ("    ", k, v)

    # State of charge
    meter_soc_json = gw.getMeterStateOfCharge().json()
    display_json("Meter state of charge (json formatted)", meter_soc_json)
    # for k, v in meter_soc_json.items():
    #     print ("    ", k, v)
    # print("Meter Power (json):", json_output)
    # print("Meter Power (json formatted):")
    # print( json.dumps(json_output, indent=4))

# Entry point of main acquisition
#  gw_addr = ip of gateway,  gw_cert_path = cert file, polling_interval = polling interval in seconds
def main(gw_addr, gw_cert_path, polling_interval):

    # local variables
    gw_url = "https://" + gw_addr
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # disabled this warning 
    gw = gateway(gw_url, gw_cert_path)
    pw_db = db(dbHost, dbDatabase, dbUser, dbPassword)   # connect to database
    pw_db.connect()
    if (trace_on):
        print('Connected to db')

    # polling flag and timer
    do_polling = True
    start_time = time.time()
    retrieved_one_time_info = False

    # Get new 
    while (do_polling):

        # time stamp of all readings in this poll cycle
        poll_timestamp = datetime.now()

        #  get these items once per polling session
        if (not retrieved_one_time_info):
            pw_db.add(poll_timestamp, "Site_Info", json.dumps(gw.getSiteInfo().json()))
            pw_db.add(poll_timestamp, "Status", json.dumps(gw.getStatus().json()))
            retrieved_one_time_info = True

        # Get these items every polling interval
        #   Grid status - Status of grid up/down, etc.
        pw_db.add(poll_timestamp, "Grid_Status", json.dumps(gw.getGridStatus().json()))

        #   Site Master - Gateway status - talking to Tesla, state
        pw_db.add(poll_timestamp, "Site_Master", json.dumps(gw.getSitemaster().json()))

        #   Meter aggregate - current solar, grid, battery production and home usage
        pw_db.add(poll_timestamp, "Meter_Aggregates", json.dumps(gw.getMeterAggregates().json()))

        #   State of charge
        pw_db.add(poll_timestamp, "Meter_State_Of_Charge", json.dumps(gw.getMeterStateOfCharge().json()))
      
        #   Display log time
        if (trace_on):
            print ("logged at", poll_timestamp.strftime("%Y-%m-%d %H:%M:%S"))

        # wait until next interval.  
        #    ---  Should I update calculations to remove time to obtain and store info?
        time.sleep(polling_interval - ((time.time() - start_time) % polling_interval))

   

# if running as main (i.e. from command line)
if __name__ == "__main__":

    # parse command line arguments
    # Use nargs to specify how many arguments an option should take.
    ap = argparse.ArgumentParser()
  
    # default of 'powerwall' reference entry in HOSTS file containing ip addr of gateway
    # default to carcert.pem as name of certificate user created (NOT CURRENLY USED)
    ap.add_argument("--gw_address",  default="powerwall", help="name or address of powerwall gateway" )
    ap.add_argument("--gw_cert",  default="cacert.pem", help="path to certification file" )
    ap.add_argument("--trace", default=True, help="Display trace information to console")
 
    # get args
    args = ap.parse_args()
    trace_on = args.trace

    # print("gw_address:", args.gw_address)
    # print("gw_cert:", args.gw_cert)
  
    main(args.gw_address, args.gw_cert, 10) # (5 * 60))  # poll every 5 minutes  (5 * 60 sec)
