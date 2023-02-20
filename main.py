from core.ice import ice_study
from model.user import User
from model.courses import Courses
from plug.Plug import Plug

@Courses
@User
@Plug
@ice_study
def main():
    ...
if __name__ == "__main__":
    main