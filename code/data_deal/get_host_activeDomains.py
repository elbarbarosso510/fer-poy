import os, sys
import re
from collections import defaultdict
import json

file = "/mnt/Work/DNS/data/active_domains/2017110400/201711040000.txt"

def ipv4_addr_check(ipAddr):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ipAddr):
        return True
    else:
        return False

def get_host_activeDomains(sips_to_find):
    '''
    {
    "1.1.1.1":{
        "www.baidu.com": ["1.1.1.1", "2.2.2.2"],
        "www.google.com": ["1.1.1.1", "2.2.2.2"],
        "www.facebook.com": ["1.1.1.1", "2.2.2.2"]
        },
    "1.2.1.1":{
        "www.baidu.com": ["1.1.1.1", "2.2.2.2"],
        "www.google.com": ["1.1.1.1", "2.2.2.2"],
        "www.facebook.com": ["1.1.1.1", "2.2.2.2"]
        },
    "1.3.1.1":{
        "www.baidu.com": ["1.1.1.1", "2.2.2.2"],
        "www.google.com": ["1.1.1.1", "2.2.2.2"],
        "www.facebook.com": ["1.1.1.1", "2.2.2.2"]
        }
    }
    '''

    host_domain_ips = defaultdict(lambda : dict())
    i = 0
    f_in = open(file, "r")
    for row in f_in:
        # i += 1
        # if i > 100:
        #     break
        items = row.strip().split(',')
        # print(items[15])
        if items[15] != "A": # only reserve the A type
            continue
        sip = items[0]
        if sip not in sips_to_find:
            continue
        domain = items[3]
        ips = items[19].split(";")

        ips = list(filter(ipv4_addr_check, ips))
        # print("{}, {}, {}".format(sip, domain, ips))

        if sip in host_domain_ips:
            domain_ips_1 = host_domain_ips[sip]
            if domain in domain_ips_1:
                domain_ips_1[domain] = domain_ips_1[domain] | set(ips)
            else:
                domain_ips_1[domain] = set(ips)
            host_domain_ips[sip] = domain_ips_1

        else:
            domain_ips = defaultdict(lambda : set())
            domain_ips[domain] = set(ips)
            host_domain_ips[sip] = domain_ips


    for sip in host_domain_ips:
        domain_ips = host_domain_ips[sip]
        for domain in domain_ips:
            host_domain_ips[sip][domain] = list(host_domain_ips[sip][domain])

    # show for comprehension
    # for sip in host_domain_ips:
    #     domain_ips = host_domain_ips[sip]
    #     print(sip + ":")
    #     for domain in domain_ips:
    #         print("\t" + domain+ ":", end='')
    #         print(domain_ips[domain])

    f_in.close()

    file_out = "201711040000_host_activeDomain_ips.json"
    f_out = open(file_out, "w")
    json.dump(host_domain_ips, f_out, indent=8)
    f_out.close()


if __name__ == "__main__":
    sips_to_find = ["116.6.44.68", "113.87.183.55"] #, "116.6.44.68", "113.87.183.52", "121.10.40.138", "121.10.40.57", "61.142.209.91", "59.42.39.207"
    get_host_activeDomains(sips_to_find)

