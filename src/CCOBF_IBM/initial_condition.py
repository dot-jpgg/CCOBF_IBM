import numpy as np

from CCOBF_IBM.parameters import DATA_COLS
from CCOBF_IBM.bootstrapping import bootstrap_data


def get_initial_condition(data, config):

    sim_df = data[DATA_COLS].copy()
    sim_df = make_age_groups(sim_df, config)
    sim_df = bootstrap_data(
        config['department_size'], sim_df, config
    )
    sim_df = sim_df.copy()
    sim_df['Time'] = 0
    sim_df['TimeJoined'] = 0

    return sim_df


def make_age_groups(data, config):

    # Make age groups.
    # -1 because age range is left-exclusive: (min, max]
    age_group_starts = np.arange(config['min_age'] - 1, config['max_age'], config['age_group_size'])

    # Find which age group each person belows to.
    ages = data['Age'].values
    age_groups = np.array([
        max([
            ag_start for ag_start in age_group_starts if (a >= ag_start) and (a < (ag_start + config['age_group_size']))
        ]) for a in ages
    ])

    data = data.copy()
    data['AgeGroup'] = age_groups
    return data


