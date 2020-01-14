import json

def save_dict(dic, file):
    dump = json.dumps(dic)
    f = open(file,"w")
    f.write(dump)
    f.close()

def load_dict(file):
    f = open(file, "r")
    dic = json.loads(f.readline())
    return dic
