from mongodb import Alerts
import bson

class WatchNotFoundException(Exception):
    '''Watch not found'''

class Alert:
    @staticmethod
    def get_all(email: str) -> list:
        with Alerts() as alerts:
#{'email': {'eq': email}}
            all_alerts = []
            for alert in alerts.find({}):
                alert['_id'] = str(alert['_id'])
                all_alerts.append(alert)

            return all_alerts

    def __init__(self, id: str):
        self.id = id

        watch = None
        with Alerts() as watches_collection:
            curs = watches_collection.find({'_id': {'$eq': id}})
            watch = list(curs)[0]
            curs.close()

        self.id = str(watch['_id'])
        self.lat = watch['lat']
        self.lng = watch['lng']
        self.accuracy = watch['accuracy']
        self.email = watch['email']
        self.name = watch['name']
        self.time = watch['time']
        self.radius = watch['radius']