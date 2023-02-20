from core.mod import mod
import os

NT = 'nt'
# 如想Windows强制运行，请把nt删掉(推荐'')或更改为任意字符

def Plug(self):
    if os.name == NT:
        self.beta = False
    if os.name == 'nt':
        self.iLog('请注意您当前在Windows环境运行，您可能需要繁琐配置环境', 2)
    if not self.beta:
        return self
    m = mod()
    self.iLog("--- Start Plug ---")
    m.add()
    self.iLog(f"Number of loaded plugins: {len(m.mod)}")
    m.run(self)
    self.iLog("---  End Plug  ---")
    return self