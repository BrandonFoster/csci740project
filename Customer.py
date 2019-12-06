from collections import deque


from numpy.random import uniform as U
from numpy.random import normal as N
from numpy.random import exponential as EXP

class Customer():
    def __init__(self):
        self.affinity = [self.sweet(), self.dry(), self.white(), self.red()]
        self.max_budget = int(round(U(0,700)))
        self.time = 0
        
    def sweet(self):
        x = (rand_bimodal(2,8)/10)
        return x if 0 < x < 10 else 0 if x < 0 else 10

    def dry(self):
        x = (rand_bimodal(2,8)/10)
        return x if 0 < x < 10 else 0 if x < 0 else 10

    def white(self):
        x = (rand_bimodal(2,8)/10)
        return x if 0 < x < 1 else 0 if x < 0 else 1

    def red(self):
        x = (rand_bimodal(2,8)/10)
        return x if 0 < x < 1 else 0 if x < 0 else 1
    def set_time(self,time):
        self.time = time



def rand_bimodal(m0, m1, s0=1, s1=1, f=U):
    p = f(0,1)
    x = p * N(m0, s0) + (1 - p) * N(m1,s1)
    return x
