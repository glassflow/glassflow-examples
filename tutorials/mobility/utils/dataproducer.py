from faker import Faker
import hashlib
import random
import string
from datetime import datetime, timedelta
from random import choice, randint
from shapely.geometry import Polygon, Point
from faker.providers import BaseProvider


class DataProducer:

    def __init__(self, name):
        self.fake = Faker()
        self.fake.add_provider(RideCompletedProvider)

    def ride_completed(self):
        event = self.fake.ride_completed(session_start_time=datetime.utcnow())
        return event


def polygon_random_points(poly):
    min_x, min_y, max_x, max_y = poly.bounds
    random_point = Point(
        [random.uniform(min_x, max_x),
         random.uniform(min_y, max_y)])
    return random_point


cities = ["Berlin", "Hamburg"]
car_categories = ["S", "M", "L"]
car_makes = ["VW", "Audi", "Seat"]

berlin_polygon = Polygon([(52.508138366861516, 13.364347207591818),
                          (52.54771901166605, 13.342460382030294),
                          (52.55450366585219, 13.409837472484396),
                          (52.47709641197807, 13.4621941924551)])
hamburg_polygon = Polygon([(53.54678834156796, 10.032488903515606),
                           (53.638891764442995, 9.978930553906231),
                           (53.60060764684186, 10.174624523632794)])


class RideCompletedProvider(BaseProvider):
    """
        A Provider for clickstream related test data.

        >>> from faker import Faker
        >>> from faker_clickstream import ClickstreamProvider
        >>> fake = Faker()
        >>> fake.add_provider(ClickstreamProvider)
        >>> fake.session_clickstream()
    """

    def user_agent(self):
        """
        Generate random user agent.

        :return: User agent string
        """
        return choice(user_agents)

    def _event_name(self):
        """
        Generate random event type name for e-commerce site.

        :return: Event type string
        """
        return "ride_completed"

    def ride_completed(self, session_start_time):
        """
        Generate random ride completed events

        """
        session_id = _get_session_id()
        incremental_delta_delay = randint(1, 60)

        event_time = _format_time(
            _get_event_time(session_start_time, delta=incremental_delta_delay))
        city = choice(cities)
        event = {
            "event_name": "ride_completed",
            "event_id": _get_session_id(),
            "timestamp": event_time,
            "city": city,
            "car_category": choice(car_categories),
            "car_make": choice(car_makes),
            "is_electric": False,
            "fuel_type": "E5",
            "current_fuel_percentage": randint(15, 30),
            "gps_cordinates": _generate_cordinates(city),
            "mobility_zone": _mobility_zone(city)
        }

        return event


def _get_session_id():
    """
    Generate session ID

    :return: Session ID string
    """
    return hashlib.sha256(
        ('%s%s%s' % (datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
                     (''.join(random.choice(string.ascii_lowercase))
                      for _ in range(10)),
                     'faker_clickstream')).encode('utf-8')).hexdigest()


def _get_product_code():
    """
    Generate random product code from range 1 to 999999.

    :return: Random integer number
    """
    return randint(1, 999999)


def _get_order_id():
    """
    Generate random order id from range 1 to 999999.

    :return: Random integer number
    """
    return randint(1, 999999)


def _get_user_id(start: int = 0, end: int = 999999):
    """
    Generate random user id from range 0 to 999999. Zero value may identify null user.

    :param start: Index start (Default: 0)
    :param end: Index end (Default: 999999)
    :return:
    """
    return randint(start, end)


def _get_event_time(start, delta):
    """
    Generate current event time, added by some delta value.

    :param delta: Delta time value in seconds
    :return: Event time
    """
    return start + timedelta(seconds=delta)


def _format_time(t):
    """
    Format time to string.

    :param t: Time object
    :return: Time string in format like 28/03/2022 23:22:15.360252
    """
    return int(round(t.timestamp()))
    #return t.strftime('%Y-%m-%dT%H:%M:%SZ')
    #return t.strftime("%d/%m/%Y %H:%M:%S.%f")


def _generate_cordinates(city):
    if city == "Berlin":
        point = polygon_random_points(berlin_polygon)
        return point.x, point.y
    elif city == "Hamburg":
        point = polygon_random_points(hamburg_polygon)
        return point.x, point.y
    else:
        return 0, 0


def _mobility_zone(city):
    if city == "Berlin":
        return "BE_%d" % randint(17, 35)
    elif city == "Hamburg":
        return "HH_%d" % randint(9, 22)
    else:
        return "Unknown"
