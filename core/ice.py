from .api import Api
from .error import Error
from .crates.Logo import Logo
from .crates.Http import Http
from .crates.Log import iLog
from .args import Args
from model.user import Header

def iLog_new(ice, iLog):
    iLog = iLog(1, "config/iLog.log")
    iLog.level = not ice.debug
    iLog.LINE = ice.debug
    iLog.MODEL = ice.debug
    iLog.PATH = ice.debug
    iLog = iLog.log
    ice.iLog = iLog

def nlog():
    ...

class ice_study:
    VERSION = """
      ___ _   _  ___  __ _ _ __
     / __| | | |/ _ \/ _` | '__|
    | (__| |_| |  __/ (_| | |
     \___|\__, |\___|\__,_|_|
          |___/\tice-study 0.0.1(Beta LTS)
    """
    def __init__(self, main=None, proxy=None, v=True):
        res = Args()
        Logo(v and res['logo'])
        self.debug = int(res['debug'])
        iLog_new(self,iLog)
        if res['v']:
            self.iLog(self.VERSION)
            quit(0)
        self.headers = Header()
        self.proxy = proxy
        self.iLog(res, 0)
        self.iLog("Welcome to " + self.VERSION)
        self.iLog(f"\nVerison: {v}\nHeader: {self.headers}\nProxy: {self.proxy}\n", 0)
    def login(self, user: str, password: str):
        data = Api.Login_fn(user, password)
        self.iLog(f"\n[POST]: {Api.Login}\nData: {data}\n", 0)
        with Http.Client(headers=self.headers, params=data, proxies=self.proxy) as r:
            res = r.post(Api.Login)
            self.iLog(f"\nRes: {res.text}\n", 0)
            if not res.json()["status"]:
                self.iLog("Login status... [False]", 4)
                self.iLog(f"Error Res: {res.text}", 4)
                quit(0)
            self.iLog("Login status... [True]")
            self.cookie = res.cookies
            self.iLog(f"\nCookie: {self.cookie}\n", 0)
            return self.cookie
