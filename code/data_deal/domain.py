class Domain:
    def __init__(self, str_domain_name):
        self._domain_name = str_domain_name
        self._ips = set()

    def __str__(self):
        return self._domain_name

    def get_domain_name(self):
        return self._domain_name

    def set_ip(self, ip):
        self._ips.add(ip)

    def set_ips(self, ips):
        for ip in ips:
            self._ips.add(ip)

    def get_ips(self):
        return self._ips




