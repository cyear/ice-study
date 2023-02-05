from core.ice import ice_study
from model.user import User

def main():
    ice = ice_study() # 支持 proxy
    user = User().new(ice)

if __name__ == "__main__":
    main()
