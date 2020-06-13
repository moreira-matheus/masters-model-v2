#!python3

from numpy import sum, log, sqrt
from numpy.random import pareto

ALPHA = 1.4654
X_MIN = 1.
ERROR = 0.0

class IncomeDist:
    alpha = ALPHA
    x_min = X_MIN
    error = ERROR
    
    @staticmethod
    def draw_income():
        return IncomeDist.x_min * (1. + pareto(IncomeDist.alpha))
    
    @staticmethod
    def estimate_params(values):
        x_min = min(values)
        n = len(values)
        alpha = n/sum(log(values) - log(x_min))
        error = alpha/sqrt(n)
        
        return alpha, x_min, error

        