import os, sys
from collections import defaultdict, Counter
from alexa_top import Alexa_top
from utils import clean_string, have_other_characters
from filter import Filter
import tldextract
import json

sys.path.append("../Gibberish-Detector/")
import pickle
import gib_detect_train

model_data = pickle.load(open('../Gibberish-Detector/gib_model.pki', 'rb'))

model_mat = model_data['mat']
threshold = model_data['thresh']
print(threshold)
# threshold = 0.05

# file = "/mnt/Work/DNS/data/nxdomains_per_5_mins/20171104/201711040000.txt"

A = Alexa_top()
F = Filter()



def get_candicate_host_domains():
    days = ["20171104"]
    hours = ['%02d'%(hour) for hour in range(24)]
    mins = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
    files = []
    for day in days:
        for hour in hours:
            for minute in mins:
                files.append("/mnt/Work/DNS/data/nxdomains_per_5_mins/"+day+"/"+ day + str(hour) + minute + ".txt" )

    for file in files:
        print(file)
        day = file.split('/')[-2]
        if not os.path.exists("/mnt/Work/DNS1/results/"+day):
            os.system("mkdir -p /mnt/Work/DNS1/results/"+day)
        file_out =  "/mnt/Work/DNS1/results/"+day+"/"+file.split('/')[-1]
        # print(file_out)

        results = defaultdict()
        sip_domains = defaultdict(lambda :set())
        with open(file) as f:
            for row in f:
                items = row.strip().split(',')
                sip = items[0]
                domain = clean_string(items[3])
                if have_other_characters(domain):
                    continue
                if F.in_tld_whitelist(domain):
                    continue
                # if F.in_CDN(domain):
                #     continue
                if F.in_disposable(domain):
                    continue
                if F.in_DHCP(domain):
                    continue
                if not A.in_alexa_top(domain):
                    sip_domains[sip].add(domain)

        count = 0
        for sip, domains in sorted(sip_domains.items(), key=lambda x: len(x[1]), reverse=True):
            # main_domains = [tldextract.extract(domain_1).domain for domain_1 in domains]
            # main_domains = ['.'.join(tldextract.extract(domain_1)[:2]).replace('.', '') for domain_1 in domains]
            domain_value = {l: int(gib_detect_train.avg_transition_prob(tldextract.extract(l).domain, model_mat) > threshold ) if len(tldextract.extract(l).domain) > 9 else 1 for l in domains}
            if len([k_v[0] for k_v in domain_value.items() if k_v[1]==0]) > 2:
            # if Counter([int(gib_detect_train.avg_transition_prob(l, model_mat) > threshold ) if len(l) > 9 else 1 for l in main_domains])[0] > 2:
                # print("{}: {}".format(sip, domains))
                results[sip] = [k_v[0] for k_v in domain_value.items() if k_v[1]==0]
                count += 1
        print(count)

        for key in results:
            results[key] = sorted(results[key], key=lambda x: len(x))

        with open(file_out, "w") as f_out:
            json.dump(results, f_out, sort_keys=True, indent=4)


if __name__ == "__main__":
    get_candicate_host_domains()
