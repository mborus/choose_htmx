import time
from collections import namedtuple

Pizza = namedtuple("Pizza", ["order_id", "name", "toppings", "description"])


class OrderedPizza:
    def __init__(self, order_id: str, customer_email: str):
        self.pizza_id = order_id
        self.ordered_at = time.time()
        self.customer_email = customer_email

    @property
    def status(self):
        wait_time_min = (time.time() - self.ordered_at) // 60
        if wait_time_min < 1:
            return "Ordered."
        elif wait_time_min < 2:
            return "Prepared."
        elif wait_time_min < 10:
            return "Baking."
        return "Done."
