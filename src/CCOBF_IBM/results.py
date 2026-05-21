import numpy as np
import matplotlib.pyplot as plt

from CCOBF_IBM.config import PROJECT_ROOT
from CCOBF_IBM.parameters import RANK, GENDER, RANKS


def get_simulation_results(out_fn):

    results = np.load(PROJECT_ROOT / 'data' / 'simulated' / f'{out_fn}.npz')
    return results['out']


def make_example_figure():

    # Get results
    example_fn = 'toy_simulation'
    results = get_simulation_results(example_fn)

    # Set up figure
    f, ax = plt.subplots()

    # Get gendered rank distribution time series
    num_times = results.shape[0]
    times = np.arange(num_times)
    avg_prop_women = np.full((num_times, len(RANKS)), np.nan, dtype=float)

    for rank_idx, rank in enumerate(RANKS):
        for time_idx, time in enumerate(times):

            annual_results = results[time]

            rank_mask = annual_results[:, RANK] == rank
            women_mask = annual_results[:, GENDER] == 1
            men_mask = annual_results[:, GENDER] == 0

            annual_women = annual_results[rank_mask & women_mask]
            annual_men = annual_results[rank_mask & men_mask]

            tot_num = annual_women.shape[0] + annual_men.shape[0]
            if tot_num > 0:
                prop_women = annual_women.shape[0] / tot_num
                avg_prop_women[time_idx, rank_idx] = prop_women
    
    # Plot
    boxplot = ax.boxplot(avg_prop_women, patch_artist=True, medianprops=dict(color='k'))
    colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    for patch, colour in zip(boxplot['boxes'], colours):
        patch.set_facecolor(colour)
    ax.set_xticklabels(['L', 'SL', 'AP', 'P'])
    ax.set_ylabel('Proportion of women')

    plt.show()