from core.ice import ice_study
from model.user import User

def main():
    ice = ice_study(True)
    User = User()
    User.new(ice.login)

if __name__ == "__main__":
    main()
