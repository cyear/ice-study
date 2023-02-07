from core.ice import ice_study
from model.user import User
from model.courses import Courses
def main():
    ice = ice_study() # 支持 proxy
    user = User().new(ice)
    courses = Courses(user).new()
if __name__ == "__main__":
    main()
