#!python3

import utils
from tqdm import tqdm
from pandas import DataFrame
from model.government import Government
from model.society import Society
from model.dists.income_dist import IncomeDist

class Simulation:
    def __init__(self, param):
        self.param = param
        self.society = None
        self.government = None

    def reset(self):
        self.society = Society()
        self.society.populate(self.param.size)
        self.government = Government()
        self.government.society = self.society

    def run_once(self, times):
        res = {}
        alphas, xs_min, errors = [], [], []
        ginis, means = [], []
        pops, gdps, revs, exps = [], [], [], []
        btms, tops = [], []
        
        self.reset()
        
        for t in range(times):
            self.society.update_all_wages()
            self.government.reset_accounts()
            
            self.government.collect_taxes()
            
            if self.param.negative_tax:
                self.government.pay_nit(self.param.exemption_quantile,
                                        self.param.subsidy_rate)
            if self.param.basic_income:
                self.government.pay_ubi(self.param.fixed_benefit,
                                        self.param.variable_benefit)

            all_incomes = self.society.get_overall_incomes()

            a, x, e = IncomeDist.estimate_params(all_incomes)
            alphas.append(a)
            xs_min.append(x)
            errors.append(e)

            ginis.append(utils.gini(all_incomes))
            gdps.append(sum(all_incomes))
            means.append(gdps[-1]/self.society.size)
            revs.append(self.government.revenue)
            exps.append(self.government.expenses)
            pops.append(self.society.size)

            btm, top = utils.bottom_top(all_incomes)
            btms.append(btm)
            tops.append(top)

            self.society.update_population()
            
        res['alpha'] = alphas
        res['x_min'] = xs_min
        res['error'] = errors
        res['gini'] = ginis
        res['mean'] = means
        res['pop'] = pops
        res['gdp'] = gdps
        res['rev'] = revs
        res['exp'] = exps
        res['btm'] = btms
        res['top'] = tops

        return DataFrame.from_dict(res, orient='columns')

    def run_many(self, runs, times):
        results = None
        for r in tqdm(range(runs)):
            res = self.run_once(times)
            
            results = res if results is None else results.add(res)

        results = results.div(runs)
        return results