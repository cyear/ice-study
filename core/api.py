class Api:
    SSL = "https://"
    HOST0 = SSL + "passport2.chaoxing.com/"
    HOST1 = SSL + "mooc1-api.chaoxing.com/"

    Login_Host = HOST0 + "fanyalogin"
    # POST 
    def Login_Data(user: str, passwd: str) -> dict:
        return {
                "fid": "-1",
                "uname": user,
                "password": passwd,
                "t": "true",
                "forbidotherlogin": "0",
                "validate": "",
                }
    Courses_Get = HOST1 + "mycourse/backclazzdata?view=json&mcode="
    # GET



