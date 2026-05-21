import numpy as np

from CCOBF_IBM.data import TOY_DATA
from CCOBF_IBM.parameters import build_config
from CCOBF_IBM.ibm import simulate
from CCOBF_IBM.post_processing import save_output


def run_ibm(data, config):

    # Set seed.
    np.random.seed(config['seed'])

    # Run and save model.
    out = simulate(data, config)
    save_output(out, config)


if __name__ == '__main__':

    # Optional kwargs to pass to the IBM.
    # e.g., custom regression formulae for promotion and attrition models.
    ibm_kwargs = {
        'promotion_formula':    'Promoted ~ C(Gender) + Age + C(RetirementAge) + C(STEM) + TimeSpentAtRank',
        'attrition_formula':    'Left ~ C(Gender) + Age + C(RetirementAge) + C(STEM) + TimeSpentAtRank',
        'out_filename':         'toy_simulation'
    }
    config = build_config(**ibm_kwargs)

    # Example simulation.
    data = TOY_DATA.copy()
    run_ibm(data, config)