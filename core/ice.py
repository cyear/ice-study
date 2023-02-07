from .api import Api
from .error import Error
from .crates.Logo import Logo
from .crates.Http import Http
from .crates.Log import iLog
from .args import args
from model.user import header
ilog = iLog(1, "config/iLog.log")

def nlog():
    ...

class ice_study:
    VERSION = "ice-study 0.0.1(Beta LTS)"
    def __init__(self, proxy=None, v=True):
        res = args()
        Logo(v and res['logo'])
        self.debug = int(res['debug'])
        self.iLog = ilog
        self.iLog.level = not self.debug
        self.iLog.LINE = self.debug
        self.iLog.MODEL = self.debug
        self.iLog.PATH = self.debug
        self.iLog = self.iLog.log
        if res['v']:
            ilog.log(self.VERSION)
            quit(0)
        self.headers = header()
        self.proxy = proxy
        self.iLog("welcome to " + self.VERSION)
        self.iLog(f"\nv: {v}\nheader: {self.headers}\nproxy: {self.proxy}\n", 0)
    def login(self, user: str, password: str):
        url = Api.Login
        data = Api.Login_fn(user, password)
        self.iLog(f"\nurl[POST]: {url}\ndata: {data}\n", 0)
        with Http.Client(headers=self.headers, params=data, proxies=self.proxy) as r:
            res = r.post(url)
            self.iLog(f"\nres: {res.text}\n", 0)
            if not res.json()["status"]:
                self.iLog("Login status... [False]", 4)
                self.iLog(f"Error Res: {res.text}", 4)
                quit(0)
            self.iLog("Login status... [True]")
            self.cookies = res.cookies
            self.iLog(f"\ncookie: {self.cookies}\n", 0)
            return self.cookies

