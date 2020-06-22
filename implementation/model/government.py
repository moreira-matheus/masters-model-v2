#!python3

from numpy import quantile
from model.data.evasion_data import EvasionData
from model.data.tax_data import TaxData

class Government:
	def __init__(self):
		self.revenue, self.expenses = 0.0, 0.0
		self.society = None
	
	def reset_accounts(self):
		self.revenue, self.expenses = 0.0, 0.0

	def collect_taxes(self):
		all_incomes = self.society.get_overall_incomes()
		
		tax_thresholds = quantile(all_incomes, q=TaxData.quantiles)
		evasion_thresholds = quantile(all_incomes, q=EvasionData.quantiles)
		
		for ind in self.society.population:
			income = ind.get_taxable_income()
			tax_level = sum(income > tax_thresholds)
			evasion_level = sum(income > evasion_thresholds)
			
			due_rate = TaxData.due_rates[tax_level]
			avg_rate = EvasionData.avg_rates[evasion_level]
			self.revenue += ind.pay_taxes(due_rate, avg_rate)

	def redistribute_revenue(self, bias):
		R = self.revenue
		N = self.society.size
		b = bias

		def pi(n):
			return (R/N**2)*(2*b*n + N - b*N)

		sorted_inds = sorted(self.society.population, key=lambda ind: ind.get_overall_income())

		for pos, ind in enumerate(sorted_inds):
			transfer = (pi(pos) + pi(pos+1))/2.
			ind.receive_transfer(transfer)

	def pay_nit(self, exemption_quantile, subsidy_rate):
		exemption_threshold = quantile(self.society.get_overall_incomes(),
									   exemption_quantile)

		for ind in self.society.population:
			income = ind.get_taxable_income()
			if income < exemption_threshold:
				benefit = subsidy_rate*(exemption_threshold - income)
				ind.receive_transfer(benefit)
				self.expenses += benefit

	def pay_ubi(self, fixed_benefit, variable_benefit):
		gdp_pc = sum(self.society.get_overall_incomes())/self.society.size
		benefit = fixed_benefit + variable_benefit * gdp_pc
		for ind in self.society.population:
			ind.receive_transfer(benefit)
			self.expenses += benefit
