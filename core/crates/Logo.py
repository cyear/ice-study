import os
def Logo(v: bool) -> bool:
    '''
    Logo printing
    '''
    if not v:
        return True
    
    # Linux
    PATH = os.path.realpath(".") + "/core/crates/Linux/Logo_linux.sh"
    os.system(f"bash {PATH}")
    return True
