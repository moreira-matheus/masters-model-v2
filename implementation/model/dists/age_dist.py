#!python3

from numpy.random import choice, randint

class AgeDist:
    num_classes = 21
    class_limits = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70,
                    75, 80, 85, 90, 95, 100, 130]
    interclass_probs = [0.07232367, 0.07847402, 0.08999339, 0.08907132,
                        0.09040454, 0.08966654, 0.08253753, 0.07280817,
                        0.06819906, 0.06203403, 0.05315908, 0.04338646,
                        0.03412278, 0.025377, 0.0196148, 0.01343838,
                        0.00873877, 0.00429598, 0.00171192, 0.0005155,
                        0.00012705]
    
    @staticmethod
    def draw_age():
        class_drawn = choice(AgeDist.num_classes, p=AgeDist.interclass_probs)
        
        return randint(low=AgeDist.class_limits[class_drawn],
                       high=AgeDist.class_limits[class_drawn+1])
