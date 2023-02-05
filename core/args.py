import argparse

def args() -> dict:
    parser = argparse.ArgumentParser(description='ice-study')
    parser.add_argument('-d','--debug', action='store_true', help='打开Debug模式')
    parser.add_argument('-n', '--no-logo', action='store_false', help='关闭Logo')
    parser.add_argument('-v','--version', action='store_true', help='Version')
    args = parser.parse_args()
    debug = args.debug
    logo = args.no_logo
    v = args.version
    return {
            'debug': debug,
            'logo': logo,
            'v': v,
            }
