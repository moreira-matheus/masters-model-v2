#!python3

from numpy.random import choice, randint

class SchoolingDist:
    schooling_age = 6

    num_classes = 6
    class_limits = [0, 1, 4, 8, 11, 15, 25]
    interclass_probs = [0.111, 0.095, 0.217, 0.139, 0.307, 0.131]
    
    @staticmethod
    def draw_schooling():
        class_drawn = choice(SchoolingDist.num_classes,
                             p=SchoolingDist.interclass_probs)
        return randint(low=SchoolingDist.class_limits[class_drawn],
                       high=SchoolingDist.class_limits[class_drawn+1])
    