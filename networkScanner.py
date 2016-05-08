import socket
import subprocess
import sys
import nmap

# Requesting for user input
remoteServer = input("Enter a remote host to scan: ")

# Finds open hosts on a subnet
lst = []
nm = nmap.PortScanner()
nm.scan(hosts=remoteServer, arguments='-n -sP -PE -PA21,23,80,3389')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
for host, status in hosts_list:
    lst.append(host)

# Sorting the ip addresses
sortedlst = []
for ip in lst:
    sortedlst.append(int(ip.split('.')[3]))
sortedlst.sort()
temp = remoteServer.split('.')
lst.clear()
for x in sortedlst:
    lst.append(temp[0]+'.'+temp[1]+'.'+temp[2]+'.'+str(x))

for ip in lst:
    print(ip)

# Searching for open ports in each host
try:
   for ip in lst:
        remoteServerIP  = socket.gethostbyname(ip)
        print ("-" * 60)
        print ("Please wait, scanning remote host", remoteServerIP)
        print ("-" * 60)
        for port in range(1,1000):  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                service = socket.getservbyport(port)
                print ("Port {}: | State: Open | Protocol: {}".format(port,service))
            sock.close()
            
except KeyboardInterrupt:
    print ("You pressed Ctrl+C")
    sys.exit()

except socket.gaierror:
    print ('Hostname could not be resolved. Exiting')
    sys.exit()

except socket.error:
    print ("Couldn't connect to server")
    sys.exit()
