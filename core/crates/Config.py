import json
def write(file: str, text: dict) -> dict:
    with open(file, 'w+') as w:
        w.write(json.dumps(text))
    return text
def read(file: str) -> dict:
    try:
        with open(file, 'r+') as r:
            return json.loads(r.read())
    except:
        return write(file, {})

