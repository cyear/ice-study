from .crates.Http import Http
from .api import Api
from .crates.Version import Version
def Vsif(version):
    n = version.split('ice-study')[-1]
    a, b, c = n.split('.')
    return int(a) + int(b) + int(c[0])
def Update(Log, U):
    if U:
        Log('检测更新...', 2)
        with Http.Client() as r:
            res = r.get(Api.Update).text
            if 'Beta' in res:
                Log('检测到Beta版本', 2)
            v = Vsif(res)
            V = Vsif(Version.version)
            Log(f"\n\n\t当前版本: {V}\n\t最新版本: {v}\n")
            if v > V:
                # Log('开始更新...')
                Log('请使用git pull手动更新！')
            else:
                Log('无需更新！')
        # quit(0)