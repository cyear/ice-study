from core.ice import ice_study
from model.user import User
from model.courses import Courses
def main():
    ice = ice_study()
    ice_User = User(ice).new()
    ice_Courses = Courses(ice_User).new()
if __name__ == "__main__":
    main()
