#
#    Gateway-comm.py
#
#   This script provides methods the communicate with the Powerwall Gateway 
#   using it's API.  This communications interface is wrapped into the 
#   class Gateway.
#
#    This work is based on this great repo of the Powerwall Gateway API
#       https://github.com/vloschiavo/powerwall2
#

#   Import libraries
import numpy
import requests
import json
import urllib3   # used to prevent display of Unverified HTTPS request warning
from datetime import datetime

#   Constants
gateway_url = ""



#   Connect and command Gateway
class gateway:

    def __init__(self, gw_url, gw_cert_path):
        self.gw_url = gw_url
        self.sess = requests.Session()    # create http requests session 
        #self.sess.cert = gw_cert_path     # set certificate for session

    # Helper functions

    # put gateway URL together with feature path to create feature URL
    def featureURL(self, feature_path):
        return self.gw_url + feature_path

   # request data from gateway
    def request_data(self, feature_path, payload):
        return self.sess.get(self.gw_url + feature_path, verify=False)  # bypass security.  FIX THIS?


    # Gateway requests
 
    # get Meter/Power output
    def getMeterAggregates(self):
        return self.request_data("/api/meters/aggregates", None) 

    # get site specific meter data
    def getMeterSite(self):
        return self.request_data("/api/meters/site", None) 

    # get solar specific meter data
    def getMeterSolar(self):
        return self.request_data("/api/meters/solar", None) 

    # get the state of charge/energy    
    def getMeterStateOfCharge(self):
        return self.request_data("/api/system_status/soe", None) 
 

    # get sitemaster info
    #   {"running":true,"uptime":"802459s,","connected_to_tesla":true}
    #   Powerwall state {running|stopped}
    #   How long the powerwall has been set to the running state {in seconds}
    #   Is the powerwall gateway connected to Tesla's servers {true|false}
    def getSitemaster(self):
        return self.request_data("/api/sitemaster", None) 

    # Powerwalls
    #   # of powerwalls
    #   serial numbers
    #   PW in sync
    #   etc.
    def getPowerwalls(self):
        return self.request_data("/api/powerwalls", None) 

    def getPowerwallsStatus(self):
        return self.request_data("/api/powerwalls/status", None)

    # Customer registration
    #   {"privacy_notice":true,"limited_warranty":true,"grid_services":null,"marketing":null,"registered":true,"timed_out_registration":false}
    def getCustReg(self):
        return self.request_data("/api/api/customer/registration", None) 

    # Grid status
    #   {"grid_status":"SystemGridConnected","grid_services_active":false}
    #   {"grid_status":"SystemGridConnected"} = grid is up
    #   {"grid_status":"SystemIslandedActive"} = grid is down
    #   {"grid_status":"SystemTransitionToGrid"} = grid is restored but not yet in sync.
    def getGridStatus(self):
        return self.request_data("/api/system_status/grid_status", None) 

    # Update status    
    #   **  REQUIRES AUTHENTICATION  **
    #   username=customer, email=your Tesla account email address, password=last 5 digits of your gateway serial number
    #   {"state":"/update_failed","info":{"status":["nonactionable"]},"current_time":1422697552910}
    def getUpdateStatus(self):
        return self.request_data("/api/system/update/status", None) 

    # site info
    # {"max_site_meter_power_kW":1000000000,"min_site_meter_power_kW":-1000000000,"nominal_system_energy_kWh":13.5,
    #   "nominal_system_power_kW":10,"site_name":"Loschiavo","timezone":"America/Los_Angeles",
    #   "grid_code":"60Hz_240V_s_UL1741SA:2016_California","grid_voltage_setting":240,"grid_freq_setting":60,
    #   "grid_phase_setting":"Split","country":"United States","state":"California","distributor":"*",
    #   "utility":"Pacific Gas and Electric Company","retailer":"*","region":"UL1741SA"}
    def getSiteInfo(self):
        return self.request_data("/api/site_info", None) 

    # site name
    # {"site_name":"Home Energy Gateway","timezone":"America/Los_Angeles"}
    def getSiteName(self):
        return self.request_data("/api/site_info/site_name", None) 

    # status
    #   {"start_time":"2019-09-23 23:38:46 +0800","up_time_seconds":"223h5m51.577762169s",
    #    "is_new":false,"version":"1.40.2","git_hash":"14f7c1769ec307bba2ea62355a09d01c8e58988c+"}
    def getStatus(self):
       return self.request_data("/api/status", None) 

    # logout - logout of Gateway web UI
    def Logout(self):
       return self.request_data("/api/logout", None) 

    # Grid faults - if it shows faults, it may have limit.  Returned [] 4 days after power outage.  
    #                  I am not sure we can depend on this to remember grid failures.
    def getGridFaults(self):
        return self.request_data("/api/system_status/grid_faults", None)

    

