import requests
import re
import os
import threading
import sys

print('''
   ___ ___         
  / __| _ \_____ __
 | (__|   / -_) V /
  \___|_|_\___|\_/ 
                   ''')
print("CRev - Reverse IP to Domain")
print("Github : IM-Hanzou\n")

url = "http://ip.yqie.com/iptodomain.aspx?ip="
file_input = input("List IPs: ")
file_result = input("Result filename: ")

try:
    threads = int(input("Thread: "))
    if threads <= 0:
        raise ValueError
except ValueError:
    print("Gimme number pls!")
    sys.exit()

if not os.path.exists(file_result):
    open(file_result, "w").close()

def reverse(ip):
    with open(file_result, "a", encoding="utf-8") as f:
        response = requests.get(url + ip)
        domains = re.findall(r'<td width="90%" class="blue t_l" style="text-align: center">(.*?)</td>', response.text)
        domains = [domain for domain in domains if re.match(r'^[\x00-\x7F]+$', domain)]
        total_domains = len(domains)
        print(f"From IP {ip} we got {total_domains} domains")
        for domain in domains:
            f.write(domain + "\n")
    
try:
    ips = []
    with open(file_input, "r") as f:
        ips = f.read().splitlines()

    threads_list = []
    for i in range(threads):
        try:
            thread = threading.Thread(target=reverse, args=(ips[i],))
            threads_list.append(thread)
            thread.start()
        except IndexError:
            break

    for thread in threads_list:
        thread.join()

except KeyboardInterrupt:
    print("\nStopped!")
finally:
    print(f"Result saved to {file_result}")
