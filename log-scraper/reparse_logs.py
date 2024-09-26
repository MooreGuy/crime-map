import sys
import sentry_sdk
import slopd_log_parse
from pymongo import MongoClient

sentry_sdk.init("https://1ffbb5ff89b440338e3112310ac30750@sentry.io/1864498")

if len(sys.argv) != 2:
    print("Usage: reparse_Logs <field to update>")
    sys.exit(1)


def reparse_entry(existing_entry):
    reparsed = slopd_log_parse.parse_entry(existing_entry['raw'])
    reparsed['_id'] = existing_entry['_id']
    return reparsed


def reparse_all(field):
    lookup = {}
    entries = map(reparse_entry, logs.find(lookup))
    for entry in entries:
        id = entry[u'_id']
        val = entry[field]
        print(f"Updating: {id}, field: {field}, val: {val}")
        existing = logs.update_one({'_id': entry[u'_id']}, {'$set': {field: entry[field]}})


client = MongoClient('mongodb', 27017)
db = client.snoopy
logs = db.police_logs
field = sys.argv[1]
reparse_all(field)
