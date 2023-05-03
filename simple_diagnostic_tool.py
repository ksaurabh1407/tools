# This is a simple python program to collect statistics from client machine
# 1. % CPU Usage
# 2. % Memory Usage
# 3. ping statistics
# 4. nslookup statistics
# 5. traceroute statistics
# 6. Time to first byte
# 7. Time to last byte
# 8. Internet Speed (download / upload)
# Before executing or compiling the script to exe, change domain value and urls value, as per your specification
# Compile to exe using python -m nuitka sdt.py --standalone --python-flag=no_site


import datetime
import psutil
import pythonping
import sys
import subprocess
import urllib
from urllib.request import urlopen
import time
import speedtest

# Set domain to collect ping, nslookup & traceroute statistics
domain = 'www.example.com'
# Set urls to collect tt1b & ttlb statistics
urls = ['https://www.example.com','https://www.livemint.com']
proxies = {'http': 'http://myproxy.example.com:1234','https': 'https://myproxy.example.com:1234'}
def main():
  print("Starting stats collection. This will take less than a minute.")
  original_stdout = sys.stdout
  with open('diagnostic.log', 'w') as f:
    sys.stdout = f  
    start_time = datetime.datetime.now()
    # Start Stats Gathering ....
    print("Staring stats collection ...")
    # Collection Start
    print ("Start Time :", start_time)
    # Collecting CPU/Memory usage metrics
    print("Collecting system vitals....")
    # Calling psutil.cpu_precent() for 4 seconds
    print('CPU usage %: ', psutil.cpu_percent(4))
    # Getting % usage of virtual_memory ( 3rd field)
    print('RAM usage %:', psutil.virtual_memory()[2])
    # Collecting ping statistics for doamin
    print ("Collecting ping statistics for", domain, "...")
    print (pythonping.ping(domain, verbose=True, count=10))
    # Performing internet spped test
    st = speedtest.Speedtest()
    print("Download speed:", st.download())
    print("Upload speed:", st.upload())
    # Collecting nslookup statistics for domain
    print ("Collecting nslookup statistics for", domain,"...")
    nslookup = subprocess.Popen(["nslookup",domain],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    linecount = 0
    for nsline in iter(nslookup.stdout.readline,""):
       linecount+=1
       print(nsline)
       if linecount >= 8:
          break
    # Collecting traceroute statistics for doamin...
    print ("Collecting traceroute statistics for",domain, "...")
    traceroute = subprocess.Popen(["tracert", '-w', '100',domain],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(traceroute.stdout.readline,""):
      print(line)
      if "Trace complete" in str(line):
       break
    # Collecting Website performance statistics based on URLs
    print ("Collecting Website performance statistics on URLs ......")
    for i in urls:
      print('tt1b for Url:', i)
      open_time = time.time()
      website = urlopen(i)
      # website = urlopen(i,proxies=proxies)
      output = website.read(1)
      close_time = time.time()
      website.close()
      print('The first byte is:',output)
      print('The time to first byte is:',round(close_time-open_time,4),'seconds')
      # Clearing cache
      print("Clearing cache .......")
      urllib.request.urlcleanup()
    for i in urls:
      print('ttlb for Url:', i)
      # passed since epoch
      open_time = time.time()
      # Obtaining the URL of website
      website = urlopen(i)
      # Read the complete website
      output = website.read()
      # Return the number of seconds
      # passed since epoch
      close_time = time.time()
      # Close the website
      website.close()
      # Subtract and print the open time
      # of website from close time
      print('The total loading time of website is',round(close_time-open_time,4),'seconds')
      # Clear cache
      print("Clearing cache .......")
      urllib.request.urlcleanup()
    end_time = datetime.datetime.now()
    total_time = end_time - start_time
    print("Total stats gathering time::",total_time)
    sys.stdout = original_stdout

    
    print("Collection complete, please share log (diagnostic.log) with system administrator. It is generated in the same folder where tool is installed.")
   

 
# __name__
if __name__=="__main__":
    main()