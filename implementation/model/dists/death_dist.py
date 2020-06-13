#!python3

from numpy.random import normal

class DeathDist:
    mean = 79.158
    std_dev = 3.979
    
    @staticmethod
    def draw_age_at_death():
        return int(normal(loc=DeathDist.mean,scale=DeathDist.std_dev))
