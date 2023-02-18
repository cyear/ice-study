from core.ice import ice_study
from model.user import User
from model.courses import Courses

@Courses
@User
@ice_study
def main():
    ...
if __name__ == "__main__":
    main
