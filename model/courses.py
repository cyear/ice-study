from core.api import Api
from core.crates.Http import Http

def courses_get(header, cookie, proxy=None):
    with Http.Client(headers=header, cookies=cookie, proxies=proxy) as r:
        res = r.get(Api.Courses_Get).json()
        return res
