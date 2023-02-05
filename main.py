from core.ice import ice_study
from model.user import User

'''
✓ cookies缓存
连续课程刷课
'''

def main():
    ice = ice_study(True)
    user = User()
    user.new(ice.login, ice.headers)

if __name__ == "__main__":
    main()
