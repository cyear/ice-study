import glob
class mod:
    def __init__(self):
        self.mod={}
    def add(self):
        for fun in glob.glob('plug/*.py'):
            if fun != 'plug/Plug.py':
                fun = fun.split('/')[1][:-3]
                exec(f'import plug.{fun}')
                self.mod[f'plug.{fun}']=eval(f'plug.{fun}')
    def run(self, cls):
        for o,i in self.mod.items():
            i.main(cls)
    def cls(self):
        for i,o in self.mod.items():
            del o
            del sys.modules[i]
            self.mod={}