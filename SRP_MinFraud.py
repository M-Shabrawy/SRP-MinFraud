import os
from minfraud import Client
import geoip2.webservice
import sys, getopt

def main(argv):
    license_key = ""
    client_id = 0
    alarm_name = "SRP Test"
    alarm_time = ""
    ip_address = ""
    log_file_path = "C:\Program Files\LogRhythm\SmartResponse Plugins\SRP-MinFraud"
    log_file = llog_file_path + "\minfraud.log"

    try:
        opts, args = getopt.getopt(argv,"hk:c:a:t:i:p:",["license_key=","client_id=","alarm_name=","alarm_time=","ip_address=","log_file_path="])
    except getopt.GetoptError:
        print('SRP_MinFraud.py -k <license_key> -c <client_id> -a <alarm_name> -t <alarm_time> -i <ip_address> -p <log_file_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('SRP_MinFraud.py -k <license_key> -c <client_id> -a <alarm_name> -t <alarm_time> -i <ip_address> -p <log_file_path>')
            sys.exit()
        elif opt in ("-k", "--license_key"):
            license_key = arg
        elif opt in ("-c", "--client_id"):
            client_id = arg
        elif opt in ("-a", "--alarm_name"):
            alarm_name = arg
        elif opt in ("-t", "--alarm_time"):
            alarm_time = arg
        elif opt in ("-i","--ip_address"):
            ip_address = arg
        elif opt in ("-p", "--log_file_path"):
            log_file_path = arg

    if os.path.isdir(log_file_path):
        print ("Output directory %s exists" % log_file_path)
    else:
        try:
            os.makedirs(log_file_path)
        except OSError:
            print ("Error Creating Output Directory %s" % log_file_path)
        else:
            print ("Successfully created Output Directory %s" % log_file_path)

    icl = Client(clientid, licensekey)
    gcl = geoip2.webservice.Client(clientid, licensekey)
    geoip = gcl.insights(ip_address)
    request = {
        'device': {
            'ip_address': ip_address,
		    'accept_language': 'en-US,en;q=0.8'
        }
    }

    insights = icl.insights(request)
    geoip = gcl.insights(ip_address)
    
    ip_anonymity = ""
    if geoip.traits.is_anonymous:
        ip_anonymity = "is_anonymous"
    elif geoip.traits.is_anonymous_vpn:
        ip_anonymity = "is_anonymous_vpn"
    elif geoip.traits.is_public_proxy:
        ip_anonymity = "is_public_proxy"
    elif geoip.traits.is_tor_exit_node:
        ip_anonymity = "is_tor_exit_node"
    result = alarm_time + "|" + alarm_name + "|" + ip_address + "|" + insights.risk_score + "|" + ip_anonymity
    print(result)
    try:
        of = open(log_file,a)
        of.write(result)
        of.close
    except OSError:
        print ("Error writing to Output file %s" % log_file_path)
    else:
        print ("Output success")

if __name__ == "__main__":
   main(sys.argv[1:])
