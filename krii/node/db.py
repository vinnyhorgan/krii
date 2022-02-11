import json
import log

class Db:
    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            f = open(self.path, "r")
            data = json.load(f)
            f.close()

            return data
        except:
            log.warn(f"Could not read {self.path}, it doesn't exist")
            return None

    def write(self, data):
        f = open(self.path, "w")
        json.dump(data, f, indent=4)
        f.close()