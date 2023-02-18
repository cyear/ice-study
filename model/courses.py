from core.api import Api
from core.crates.Http import Http
class Courses:
    def __init__(self, User=None):
        if User:
            self.User = User
            self.iLog = User.iLog
            self.new()
    def new(self) -> object:
        self.iLog("Courses_Get... [OK]")
        self.courses_format()
        self.courses_select()
        self.course_get()
        return self
    def courses_get(self, header, cookie, proxy=None) -> dict:
        with Http.Client(headers=header, cookies=cookie, proxies=proxy) as r:
            self.courses = r.get(Api.Courses_Get).json()
            return self.courses
    def courses_format(self):
        cache = []
        for i in self.User.courses['channelList']:
            if 'course' in i['content']:
                cache.append({
                    'classid': i['key'],
                    'cpi': i['cpi'],
                    'name': i['content']['course']['data'][0]['name'],
                    'teacher': i['content']['course']['data'][0]['teacherfactor']
                    })
        self.iLog(cache, 0)
        self.courses_format_course = cache
        self.iLog("Courses_Format... [OK]")
    def courses_select(self):
        for i in range(len(self.courses_format_course)):
            o = self.courses_format_course[i]
            self.User.Format_list(i, f"{o['classid']} - {o['name']} - {o['teacher']}")
        self.iLog("Tips: This can be multiple choice, serial number space separate.")
        try:
            n = input("Input: ").split(" ")
            n_ = []
            for i in range(len(n)):
                n_ += [o for o in range(int(n[i-1]), int(n[i+1])+1)] if n[i] == '-' else [int(n[i])]
                self.iLog(n_, 0)
            n_ = list(set(n_))
            n_.sort()
        except: quit(1)
        self.course_select = [self.courses_format_course[int(i)] for i in n_]
        self.iLog(self.course_select, 0)
    def course_get(self):
        self.course = []
        with Http.Client(headers=self.User.ice.headers, cookies=self.User.cookie) as r:
            def return_course(d: dict) -> dict:
                try: self.iLog(f"Get Course name: {d['data'][0]['course']['data'][0]['name']}... [OK]")
                except: 
                    self.iLog("Get Course name... [Error]", 3)
                    self.iLog("Please check iLog.txt or open Debug", 4)
                    quit(1)
                return d
            self.course = [return_course(r.get(Api.Course_Get + Api.Course_GET_fn(i['classid'], i['cpi'])).json()) for i in self.course_select]
            self.iLog(self.course, 0)
            return self.course
