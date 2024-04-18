"""
generate fake events
"""

import random
from faker import Faker


class DataGenerator:

    def __init__(self):
        self.fake = Faker()
        self.userid = 0
        self.channelid = 0
        self.genre = ""
        self.lastactive = None
        self.title = ""
        self.watchfrequency = 0
        self.etags = None

    def generate_record(self):
        data = {
            "event_id":
            self.fake.uuid4(),
            "userid":
            self.fake.uuid4(),
            "channelid":
            self.fake.pyint(min_value=1, max_value=50),
            "genre":
            random.choice(["thriller", "comedy", "romcom", "fiction"]),
            "lastactive":
            self.fake.date_time_between(start_date="-10m",
                                        end_date="now").isoformat(),
            "title":
            self.fake.name(),
            "watchfrequency":
            self.fake.pyint(min_value=1, max_value=10),
        }
        return data
