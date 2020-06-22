#!python3

class Param:
    def __init__(self):
        self.size = 0
        self.bias = 0.0

        self.negative_tax = False
        self.subsidy_rate = 0.0
        self.exemption_quantile = 0.0

        self.basic_income = False
        self.fixed_benefit = 0.0
        self.variable_benefit = 0.0

    def __str__(self):
        s = '\n-> Parameters:\n'
        s+= 'Initial Size: ' + str(self.size) + '\n'
        s+= 'Govt. Bias: ' + str(self.bias) + '\n'
        s+= 'Negative Income Tax: ' + str(self.negative_tax) + '\n'
        s+= '\tExemption Quantile: ' + str(self.exemption_quantile) + '\n'
        s+= '\tSubsidy Rate: ' + str(self.subsidy_rate) + '\n'
        s+= 'Basic Income: ' + str(self.basic_income) + '\n'
        s+= '\tFixed Benefit: ' + str(self.fixed_benefit) + '\n'
        s+= '\tVariable Benefit: ' + str(self.variable_benefit) + '\n\n'
        return s

if __name__=='__main__':
    print(Param())