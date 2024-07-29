import tldextract

file_disposables = ["/mnt/Work/DNS/data/disposable_data/dis.txt", "/mnt/Work/DNS/data/disposable_data/disposable_byme.txt"]
file_tld_whitelists = ["/mnt/Work/DNS/data/disposable_data/tld_whitelist.txt"]
file_CDNs = ["/mnt/Work/DNS/data/CDN/"+ i for i in ["cdn_whitelist.txt", "cdnList_1.csv", "CDN_byme.txt", "cdn-domain.txt"]]
file_DHCPs = ["/mnt/Work/DNS/data/disposable_data/to_drop_data.txt"]

class Filter:
    def __init__(self):
        self._disposable = set()
        self._tld_whitelist = set()
        self._CDN = set()
        self._DHCP = set()

        self.load_disposable()
        self.load_tld_whitelist()
        self.load_CDN()
        self.load_DHCP()


    def load_disposable(self):
        for file in file_disposables:
            with open(file, "r") as f:
                for row in f:
                    self._disposable.add(row.strip().split()[0])

    def load_tld_whitelist(self):
        for file in file_tld_whitelists:
            with open(file, "r") as f:
                for row in f:
                    self._tld_whitelist.add(row.strip().split()[0])

    def load_CDN(self):
        for file in file_CDNs:
            with open(file, "r") as f:
                for row in f:
                    self._CDN.add(row.strip().split()[0])

    def load_DHCP(self):
        for file in file_DHCPs:
            with open(file) as f:
                for row in f:
                    self._DHCP.add(row.strip().split()[0])

    def in_disposable(self, domain):
        for d in self._disposable:
            if domain.endswith(d):
                return True
        return False

    def in_tld_whitelist(self, domain):
        ext = tldextract.extract(domain)
        if ext.suffix in self._tld_whitelist:
            return True
        return False

    def in_CDN(self, domain):
        for d in self._CDN:
            if domain.endswith(d):
                return True
        return False

    def in_DHCP(self, domain):
        for d in self._DHCP:
            if domain.endswith(d):
                return True
        return False

if __name__ == "__main__":
    # domain = "www.gg.pro"
    # domain = "gg.zhimg.com"
    domain = "123.123.123.2.ip6.arpa"
    F = Filter()
    # print(F.in_tld_whitelist(domain))
    # print(F.in_CDN(domain))
    print(F.in_disposable(domain))




