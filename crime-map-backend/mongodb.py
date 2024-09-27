from pymongo import MongoClient

class Collection:
    def __init__(self):
        self.client = None
        self.name = None

    def __enter__(self):
        self.client = MongoClient('mongodb', 27017)
        return self.client.snoopy[self.name]

    def __exit__(self, type, value, traceback):
        self.client.close()

class Alerts(Collection):
    def __init__(self):
        self.client = None
        self.name = "alerts"

class PoliceLogs(Collection):
    def __init__(self):
        self.client = None
        self.name = "police_logs"