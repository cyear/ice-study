import time
# from model.courses import Courses
from model.enc import enc
class Api:
    SSL = "https://"
    HTTP = "http://"
    HOST = HTTP + "www.iceh2o1.top/"
    HOST0 = SSL + "passport2.chaoxing.com/"
    HOST1 = SSL + "mooc1-api.chaoxing.com/"
    HOST2 = SSL + "passport2-api.chaoxing.com/"

    Update = HOST + "update"

    Login = HOST0 + "fanyalogin"
    # POST 账密登录
    def Login_fn(user: str, passwd: str) -> dict:
        return {
                "fid": "-1",
                "uname": user,
                "password": passwd,
                "t": "true",
                "forbidotherlogin": "0",
                "validate": "",
                }

    Login_sms = HOST2 + "api/sendcaptcha"
    # POST 验证码登录
    def Login_sms_fn(to: str, countrycode=86, enc=enc()):
        return {
                "to": str(to),
                "countrycode": str(countrycode),
                "time": enc[0],
                "enc": enc[1],
                }

    Courses_Get = HOST1 + "mycourse/backclazzdata?view=json&mcode="
    # GET 获取课程

    Course_Get = HOST1 + "gas/clazz?fields=id,bbsid,classscore,isstart,allowdownload,chatid,name,state,isfiled,visiblescore,begindate,coursesetting.fields(id,courseid,hiddencoursecover,coursefacecheck),course.fields(id,name,infocontent,objectid,app,bulletformat,mappingcourseid,imageurl,teacherfactor,jobcount,knowledge.fields(id,name,indexOrder,parentnodeid,status,layer,label,jobcount,begintime,endtime,attachment.fields(id,type,objectid,extension).type(video)))&view=json"
    #GET 获取课程详情
    def Course_GET_fn(classid, cpi):
        #?id=61101124&personid=250862560
        data = f"&id={classid}&personid={cpi}"
        return data

    Course_Get_Info = HOST1 + "gas/knowledge"
    # GET Course Info
    def Course_Get_Info_fn(classid, courseid, i_enc=enc()):
        return {
                "id": classid,
                "courseid": courseid,
                "fields": "id,parentnodeid,indexorder,label,layer,name,begintime,createtime,lastmodifytime,status,jobUnfinishedCount,clickcount,openlock,card.fields(id,knowledgeid,title,knowledgeTitile,description,cardorder).contentcard(all)",
                "view": "json",
                "token": "4faa8662c59590c6f43ae9fe5b002b42",
                "_time": i_enc[0],
                "inf_enc": i_enc[1]
                }