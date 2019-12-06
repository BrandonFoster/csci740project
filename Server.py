import numpy as np
import math


class Server:

    def __init__(self, next_time):
        self.next_time = next_time
        self.time = 0
        self.customer = None
