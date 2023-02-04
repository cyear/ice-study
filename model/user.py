'''
Login encryption thanks to 'Samueli924/chaoxing'
    Project(https://github.com/Samueli924/chaoxing)
'''
from core.crates.Config import write, read
from binascii import b2a_hex
from pyDes import des, PAD_PKCS5
import getpass, random, secrets
def header() -> dict:
    return {
        'User-Agent': f'Dalvik/2.1.0 (Linux; U; Android {random.randint(9, 12)}; MI{random.randint(10, 12)} Build/SKQ1.210216.001) (device:MI{random.randint(10, 12)}) Language/zh_CN com.chaoxing.mobile/ChaoXingStudy_3_5.1.4_android_phone_614_74 (@Kalimdor)_{secrets.token_hex(16)}',
        'X-Requested-With': 'com.chaoxing.mobile'
        }
def user_hide(user: str) -> str:
    return user[0:3] + "****" + user[-4:]
def f_list(k, v) -> None:
    print(f"|\t{k}| {v}\t|")
class User:
    def __init__(self) -> None:
        self.FILE = "config/users.json"
    def new(self, Login) -> dict:
        self.user = read(self.FILE)
        self.stdin()
        self.new_cookie(Login)
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
        passwd = b2a_hex(des("u2oh6Vu^", "u2oh6Vu^", pad=None,padmode=PAD_PKCS5).encrypt(passwd, padmode=PAD_PKCS5)).decode("utf-8")
        self.user[user] = passwd
        return self._write(self.user)
    def remove(self, user) -> dict:
        del(self.user[user])
        return self.user
    def new_cookie(self, Login):
        k = list(self.user.keys())
        for i in range(len(k)):
            f_list(i, k[i])
        n = int(input("Input: "))
        user = k[n]
        passwd = self.user[user]
        self.cookie = Login(user, passwd)
        return self.cookie
