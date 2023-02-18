from core.mod import mod
def Plug(self):
    m = mod()
    self.iLog("--- Start Plug ---")
    m.add()
    self.iLog(f"Number of loaded plugins: {len(m.mod)}")
    m.run(self)
    self.iLog("---  End Plug  ---")
    return self