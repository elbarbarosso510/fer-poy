import tldextract

file = "/mnt/Work/DNS/data/benignlist/alexa_top_2017_325.csv"

class Alexa_top:
    def __init__(self):
        self._alexa_top = set()
        self.load_alexa_top()

    def load_alexa_top(self):
        with open(file, "r") as f:
            for row in f:
                self._alexa_top.add(row.split()[0])

    def in_alexa_top(self, domain):
        ext = tldextract.extract(domain)
        if ext.suffix in self._alexa_top or '.'.join(ext[-2:]) in self._alexa_top:
            # print("in alexa top")
            return True
        return False

if __name__ == "__main__":
    A = Alexa_top()
    domain = "www.baidu.com"
    A.in_alexa_top(domain)