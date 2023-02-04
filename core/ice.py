from .api import Api
from .error import Error
from .crates.Logo import Logo
from .crates.Http import Http
from model.user import header
class ice_study:
    def __init__(self, v):
        Logo(v)

    def login(self, user: str, password: str) -> dict:
        url = Api.Login_Host
        data = {
                "fid": "-1",
                "uname": user,
                "password": password,
                # Password is encrypted
                "t": "true",
                "forbidotherlogin": "0",
                "validate": "",
                }
        with Http.Client(headers=header(), params=data) as r:
            res = r.post(url)
            print("Login res: ", res.json()["status"])
            return res.cookies

