'''
Login and encryption thanks to 'Samueli924/chaoxing'
    Project(https://github.com/Samueli924/chaoxing)
'''
from core.crates.Config import Write, Read
from core.crates.Http import Http
from core.api import Api
from pyDes import des, PAD_PKCS5
from .enc import enc
from .courses import Courses
import getpass, random, secrets

def Header() -> dict:
    return {
        'User-Agent': f'Dalvik/2.1.0 (Linux; U; Android {random.randint(9, 12)}; MI{random.randint(10, 12)} Build/SKQ1.210216.001) (device:MI{random.randint(10, 12)}) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_5.1.4_android_phone_614_74 (@Kalimdor)_{secrets.token_hex(16)}',
        'X-Requested-With': 'com.chaoxing.mobile'
        }
def User_hide(user: str) -> str:
    return user[0:3] + "****" + user[-4:]
def Format_list(k, v):
    print(f"| {k}\t| {v}\t|")
def Cookie_validity(header, cookie) -> bool:
   res = Courses().courses_get(header, cookie)
   return bool(res['result'])

class User:
    def __init__(self, ice):
        self.FILE = "config/users.json"
        self.FILE_COOKIE = "config/cookies.json"
        self.ice = ice
        self.iLog = ice.iLog
        self.Format_list = Format_list
        self.Courses = Courses()
    def new(self) -> object:
        self.users = Read(self.FILE)
        self.cookies = Read(self.FILE_COOKIE)
        self.stdin()
        self.user_select()
        self.new_cookie()
        return self
    def new_re(self):
        self.iLog(self.new_cookie(), 0)
    def stdin(self) -> dict:
        try:
            n = int(input("Please select:\n\t1. Add User\n\t2. Login\n\t3. Del User\n\tN. Exit\nInput: "))
            def n1(): return self.add(input("User: "), getpass.getpass("Passwd: "))
            def n2(): return {}
            def n3(): self.iLog(self.remove(self.user_select()), 0)
            return [0, n1, n2, n3][n]()
        except:
            quit(1)
    def add(self, user, passwd) -> dict:
        self.users[user] = des("u2oh6Vu^", "u2oh6Vu^", pad=None,padmode=PAD_PKCS5).encrypt(passwd, padmode=PAD_PKCS5).hex()
        return Write(self.FILE, self.users)
    def remove(self, Null=None) -> dict:
        del(self.users[self.user])
        Write(self.FILE, self.users)
        return self.users
    def user_select(self, k=0):
        if not k:
            k = list(self.users.keys())
        for i in range(len(k)):
            self.Format_list(i, User_hide(k[i]))
        try:
            n = int(input("Input: "))
            self.user = k[n]
            self.passwd = self.users[self.user]
        except: quit(1)
    def new_cookie(self):
        def cookie_validity(self):
            self.courses = self.Courses.courses_get(self.ice.headers, self.cookies[self.user])
            self.iLog(self.courses, 0)
            self.cookie = self.cookies[self.user]
            if self.courses['result']:
                self.iLog("Cookie...  [OK]")
                self.iLog(self.cookie, 0)
            else:
                self.iLog("Cookie... [Error]")
                quit(1)
        if self.user in self.cookies.keys():
            cookie_validity(self)
        else:
            self.iLog("Cookie... [Refresh]", 2)
            self.cookie = self.ice.login(self.user, self.passwd)
            self.iLog(self.cookie, 0)
            self.cookies[self.user] = dict(self.cookie)
            self.iLog(Write(self.FILE_COOKIE, self.cookies), 0)
            cookie_validity(self)
