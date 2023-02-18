import os
def Logo(v: bool) -> bool:
    '''
    Logo printing
    '''
    if not v or os.name == 'nt':
        return True
    
    # Linux
    import core.crates.Linux.Logo_linux
    #PATH = os.path.realpath(".") + "/core/crates/Linux/Logo_linux.sh"
    #os.system(f"bash {PATH}")
    return True
