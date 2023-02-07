from core.api import Api
from core.crates.Http import Http

class Courses:
    def __init__(self, User=None) -> None:
        self.User = User
    def new(self) -> object:
        self.iLog = self.User.iLog
        self.iLog("Courses_Get... [OK]")
        self.courses = self.User.Courses.courses
        self.f_list = self.User.f_list
        return self
    def courses_get(self, header, cookie, proxy=None) -> dict:
        with Http.Client(headers=header, cookies=cookie, proxies=proxy) as r:
            self.courses = r.get(Api.Courses_Get).json()
            return self.courses
    def courses_format(self):
        ...
