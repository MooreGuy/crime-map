import sentry_sdk
import io
import json
import sys
import logging
import slopd_log_parse
import pycurl
from pymongo import MongoClient
from kafka import KafkaProducer

sentry_sdk.init("https://1ffbb5ff89b440338e3112310ac30750@sentry.io/1864498")

logging.basicConfig()
logger = logging.getLogger('Scraper')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class Scraper:
    def __init__(self):
        if 'unittest' not in sys.modules:
            self.producer = KafkaProducer(bootstrap_servers='kafka-cluster:9092',
                                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))

            logger.info("Connecting to mongodb")
            client = MongoClient('mongodb')
            self.logs = client.snoopy.police_logs
        else:
            self.logs = None

        self.pulled_log = []

    def fetch_log(self):
        buffer = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://pdreport.slocity.org/policelog/rpcdsum.txt')
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue().decode('iso-8859-1')
        self.raw_log = body

    def parse_logs(self):
        logger.info("Parsing logs")
        parsed = slopd_log_parse.parse_log(self.raw_log)
        logger.info("Logs parsed")

        self.pulled_log = list(parsed)

    def send_out_logs(self):
        totalInserted = 0
        totalEntries = 0

        entered = [self.handle_entry(entry) for entry in self.pulled_log]
        totalEntries = len(entered)
        totalInserted = len(list(filter(None, entered)))

        logger.info(f"finished scraping. Created entries: {str(totalInserted)}. Total scraped: {str(totalEntries)}")

        return (totalEntries, totalInserted)

    def handle_entry(self, entry):
        existing = self.logs.find_one({"report_number": entry["report_number"]})
        if not existing:
            id = self.logs.insert_one(entry).inserted_id
            logger.info(f"{id} - inserting entry")
            self.send_log_to_kafka(id)

            return True
        return False

    def send_log_to_kafka(self, id):
        try:
            # producer.send('log-entries', {'id': id})
            logger.info(f"{id} - not sent to kafka broker")
        except Exception as e:
            sentry_sdk.capture_exception(e)


if __name__ == "__main__":
    scraper = Scraper()
    scraper.fetch_log()
    scraper.parse_logs()
    scraper.send_out_logs()
    for handler in logger.handlers:
        handler.close()
