from core.ice import ice_study
from model.user import User
from model.courses import Courses
from model.course import Course
from plug.Plug import Plug

@Course
@Courses
@User
@Plug
@ice_study
def main():
    ...
if __name__ == "__main__":
    main