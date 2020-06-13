#!python3

from numpy import exp
from numpy.random import uniform

RHO_S = 0.107
BETA_0, BETA_1 = 0.081, -0.0012

class Individual:
    def __init__(self):
        self.initial_income = 0.0
        self.current_income = {'wages': 0.0, 'transfers': 0.0}
        self.current_age = 0
        self.age_at_death = 0
        self.schooling = 0
    
    def grow_older(self):
        self.current_age = self.current_age + 1
    
    def is_alive(self):
        return self.current_age < self.age_at_death
    
    def get_taxable_income(self):
        return self.current_income['wages']
    
    def get_overall_income(self):
        return sum(self.current_income.values())
    
    def reset_income(self):
        self.current_income = {source: 0.0 \
                               for source in self.current_income.keys()}
        
    def update_wage(self, schooling_age=6):
        self.reset_income()
        
        is_working = self.current_age > (self.schooling+schooling_age)
        x = is_working * (self.current_age-(self.schooling+schooling_age))
        s = is_working * self.schooling + \
            (not is_working) * max([self.current_age - schooling_age])
        
        self.current_income['wages'] = self.initial_income * \
            ((not is_working) + is_working*exp(RHO_S*s+BETA_0*x+BETA_1*x**2))
    
    def receive_transfer(self, transfer):
        self.current_income['transfers'] = self.current_income['transfers'] + \
            transfer
    
    def pay_taxes(self, due_rate, avg_rate):
        lo, hi = sorted([due_rate, 2*avg_rate - due_rate])
        actual_rate = max([0.0, uniform(lo, hi)])
        taxes = actual_rate * self.current_income['wages']
        self.current_income['wages'] = self.current_income['wages'] -\
            taxes
        
        return taxes
    
    def __str__(self):
        st = '\nINDIVIDUAL {}: '.format(id(self))
        st+= '\n\tInitial income: ' + str(self.initial_income)
        st+= '\n\tCurrent income: ' + str(self.current_income)
        st+= '\n\tCurrent age: ' + str(self.current_age)
        st+= '\n\tAge at death: ' + str(self.age_at_death)
        st+= '\n\tSchooling: ' + str(self.schooling)
        
        return st

if __name__ == '__main__':
    ind = Individual()
    
    ind.initial_income = 100.0
    ind.schooling = 10
    ind.current_age = 25
    ind.age_at_death = 78
    ind.update_wage()
    
    ind.receive_tranfer(10)
    print(ind)
    print('\nTaxes: ', ind.pay_taxes(0.15, 0.05))