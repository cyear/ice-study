'''
Login and enc encryption thanks to 'Samueli924/chaoxing'
    Project(https://github.com/Samueli924/chaoxing)
'''
from core.crates.Config import write, read
from core.crates.Http import Http
from core.api import Api
from pyDes import des, PAD_PKCS5
from .enc import enc
from .courses import courses_get
import getpass, random, secrets
def header() -> dict:
    return {
        'User-Agent': f'Dalvik/2.1.0 (Linux; U; Android {random.randint(9, 12)}; MI{random.randint(10, 12)} Build/SKQ1.210216.001) (device:MI{random.randint(10, 12)}) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_5.1.4_android_phone_614_74 (@Kalimdor)_{secrets.token_hex(16)}',
        'X-Requested-With': 'com.chaoxing.mobile'
        }
def user_hide(user: str) -> str:
    return user[0:3] + "****" + user[-4:]
def f_list(k, v) -> str:
    s = f"|\t{k}| {v}\t|"
    print(s)
    return s
def cookie_validity(header, cookie) -> bool:
   res = courses_get(header, cookie)
   return bool(res['result'])
class User:
    def __init__(self):
        self.FILE = "config/users.json"
        self.FILE_COOKIE = "config/cookies.json"
    def new(self, ice) -> object:
        self.users = read(self.FILE)
        self.cookies = read(self.FILE_COOKIE)
        self.ice = ice
        self.iLog = ice.iLog
        self.stdin()
        self.headers = self.ice.headers
        self.user_select()
        self.iLog(self.new_cookie(), 0)
        return self
    def new_re(self):
        self.iLog(self.new_cookie(), 0)
    def _write(self, text: dict) -> dict:
        return write(self.FILE, text)
    def stdin(self) -> dict:
        try:
            n = int(input("Please select:\n\t1. Add User\n\t2. Login\n\t3. Del User\n\tN. Exit\nInput: "))
        except:
            quit(0)
        def n1():
            user, passwd = input("User: "), getpass.getpass("Passwd: ")
            '''
            Tips:
                1.About the password:
                    Ever used ssh? yeah! That's what he didself.
            '''
            return self.add(user, passwd)
        def n2():
            return {}
        def n3():
            self.user_select()
            self.iLog(self.remove(), 0)
        l = [n1, n2, n3]
        if n > 3:
            quit(0)
        return l[n-1]()
    def add(self, user, passwd) -> dict:
        self.users[user] = des("u2oh6Vu^", "u2oh6Vu^", pad=None,padmode=PAD_PKCS5).encrypt(passwd, padmode=PAD_PKCS5).hex()
        return self._write(self.users)
    def remove(self) -> dict:
        del(self.users[self.user])
        write(self.FILE, self.users)
        return self.users
    def user_select(self):
        k = list(self.users.keys())
        for i in range(len(k)):
            f_list(i, k[i])
        try:
            n = int(input("Input: "))
        except:
            quit(1)
        self.user = k[n]
        self.passwd = self.users[self.user]
    def new_cookie(self) -> dict:
        self.proxy = self.ice.proxy
        if self.user in self.cookies.keys():
            res = courses_get(self.headers, self.cookies[self.user])
            self.iLog(res, 0)
            self.courses = res
            self.cookie = self.cookies[self.user]
            # if cookie_validity(header, self.cookies[user]):
            if res['result']:
                self.iLog("Cookie...  [OK]")
                return self.cookies[self.user]
        self.iLog("Cookie... [Refresh]", 2)
        self.cookie = self.ice.login(self.user, self.passwd)
        self.cookies[self.user] = dict(self.cookie)
        self.iLog(write(self.FILE_COOKIE, self.cookies), 0)
        return dict(self.cookie)
