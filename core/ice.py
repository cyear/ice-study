from .api import Api
from .error import Error
from .crates.Logo import Logo
from .crates.Http import Http
from model.user import header
class ice_study:
    def __init__(self, v):
        Logo(v)
        self.headers = header()
        print("welcome to ice-study 0.0.1(Beta LTS)")
    def login(self, user: str, password: str):
        url = Api.Login_Host
        data = Api.Login_Data(user, password)
        with Http.Client(headers=self.headers, params=data) as r:
            res = r.post(url)
            print("Login res: ", res.json()["status"])
            self.cookies = res.cookies
            return self.cookies

