#!python3

from numpy import quantile
from model.individual import Individual
from model.dists.age_dist import AgeDist
from model.dists.death_dist import DeathDist
from model.dists.income_dist import IncomeDist
from model.dists.schooling_dist import SchoolingDist
from model.data.birth_data import BirthData

class Society:
    def __init__(self):
        self.population = []
        self.size = 0
    
    def populate(self, size):
        for _ in range(size):
            ind = Individual()
            
            age1, age2 = AgeDist.draw_age(), DeathDist.draw_age_at_death()
            ind.current_age, ind.age_at_death = sorted([age1, age2])
            ind.initial_income = IncomeDist.draw_income()
            ind.schooling = SchoolingDist.draw_schooling()
            
            self.population.append(ind)
        
        self.size = len(self.population)

    def get_overall_incomes(self):
        return [ind.get_overall_income() for ind in self.population]

    def update_all_wages(self):
        for ind in self.population:
            ind.update_wage(SchoolingDist.schooling_age)

    def update_population(self):
        deaths = [0] * len(BirthData.rates)
        incomes = [0.] * len(BirthData.rates)
        thresholds = quantile(self.get_overall_incomes(),
                              q=BirthData.quantiles)
        
        for ind in self.population:
            ind.grow_older()
            if not ind.is_alive():
                income = ind.get_overall_income()
                level = sum(income > thresholds)
                deaths[level] += 1
                incomes[level] += income
                self.population.remove(ind)
            
        births = [int(d*(1.+r)) for d,r in zip(deaths, BirthData.rates)]

        for birth, income in zip(births, incomes):
            if birth > 0:
                for _ in range(birth):
                    ind = Individual()
                    ind.initial_income = income/birth
                    ind.current_age = 0
                    ind.age_at_death = DeathDist.draw_age_at_death()
                    ind.schooling = SchoolingDist.draw_schooling()
                    self.population.append(ind)

        self.size = len(self.population)

    def __str__(self):
        st = '\nSOCIETY {}:'.format(id(self))
        st+= '\n\tSize: ' + str(self.size)
        
        return st

if __name__ == '__main__':
    soc = Society()
    soc.populate(10)
    print(soc)
    soc.update_all_wages()
    print('All incomes: ', soc.get_overall_incomes())
