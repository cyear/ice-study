class Api:
    SSL = "https://"
    HOST0 = SSL + "passport2.chaoxing.com/"
    HOST1 = SSL + "mooc1-api.chaoxing.com/"
    def __init__(self) -> None:
        ...

    Login = HOST0 + "fanyalogin"
    # POST 登录
    def Login_fn(user: str, passwd: str) -> dict:
        return {
                "fid": "-1",
                "uname": user,
                "password": passwd,
                "t": "true",
                "forbidotherlogin": "0",
                "validate": "",
                }
    Courses_Get = HOST1 + "mycourse/backclazzdata?view=json&mcode="
    # GET 获取课程
    Course_Get = HOST1 + "gas/clazz?fields=id,bbsid,classscore,isstart,allowdownload,chatid,name,state,isfiled,visiblescore,begindate,coursesetting.fields(id,courseid,hiddencoursecover,coursefacecheck),course.fields(id,name,infocontent,objectid,app,bulletformat,mappingcourseid,imageurl,teacherfactor,jobcount,knowledge.fields(id,name,indexOrder,parentnodeid,status,layer,label,jobcount,begintime,endtime,attachment.fields(id,type,objectid,extension).type(video)))&view=json"
    #GET 获取课程详情
    def Course_GET_fn(classid, cpi):
        #?id=61101124&personid=250862560
        data = f"&id={classid}&personid={cpi}"
