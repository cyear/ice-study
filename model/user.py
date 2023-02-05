'''
Login encryption thanks to 'Samueli924/chaoxing'
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
def cookie_validity(cookie) -> bool:
    ...
class User:
    def __init__(self):
        self.FILE = "config/users.json"
        self.FILE_COOKIE = "config/cookies.json"
    def new(self, Login, headers) -> dict:
        self.user = read(self.FILE)
        self.cookies = read(self.FILE_COOKIE)
        self.stdin()
        self.new_cookie(Login, headers)
        return self.cookie
    def _write(self, text: dict) -> dict:
        return write(self.FILE, text)
    def stdin(self) -> dict:
        try:
            n = int(input("Please select:\n\t1. Add User\n\t2. Login\n\t3. Del User\n\tN. Exit\nInput: "))
        except:
            quit(0)
        if n==1:
            user, passwd = input("User: "), getpass.getpass("Passwd: ")
            '''
            Tips:
                1.About the password:
                    Ever used ssh? yeah! That's what he didself.
            '''
            return self.add(user, passwd)
        elif n==2:
            ...
        elif n==3:
            self.remove(input("User:"))
        else:
            quit(0)
        return {}
    def add(self, user, passwd) -> dict:
        passwd = des("u2oh6Vu^", "u2oh6Vu^", pad=None,padmode=PAD_PKCS5).encrypt(passwd, padmode=PAD_PKCS5).hex()
        self.user[user] = passwd
        return self._write(self.user)
    def remove(self, user) -> dict:
        del(self.user[user])
        return self.user
    def new_cookie(self, Login, header) -> dict:
        k = list(self.user.keys())
        for i in range(len(k)):
            f_list(i, k[i])
        n = int(input("Input: "))
        user = k[n]
        passwd = self.user[user]
        # cookie = read(self.FILE_COOKIE)
        if user in self.cookies.keys():
            res = courses_get(header, self.cookies[user])
            self.courses = res
            self.cookie = self.cookies[user]
            if res['result']:
                print("Cookie 有效")
            return self.cookies[user]
        self.cookie = Login(user, passwd)
        #! if cookie 
        self.cookies[user] = dict(self.cookie)
        write(self.FILE_COOKIE, self.cookies)
        return dict(self.cookie)
