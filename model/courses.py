from core.api import Api
from core.crates.Http import Http

def courses_get(header, cookie):
    with Http.Client(headers=header, cookies=cookie) as r:
        res = r.get(Api.Courses_Get).json()
        #print(res)
        return res
