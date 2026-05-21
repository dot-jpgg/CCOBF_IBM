import numpy as np
import pandas as pd

from itertools import product
from CCOBF_IBM.parameters import ALL_HIRING_INTERVENTIONS



def bootstrap_data(n, data, config):
    
    data = data.copy()

    # Adjust hiring pool composition and shuffle variables as per config.
    data = change_hiring_pool_composition(data, config)
    if config['hiring_interventions']:
        data = shuffle_vars(data, config)

    # Remove age group (don't need it for the simulation, only bootstrapping).
    data = data.drop(columns='AgeGroup')    

    # Get n bootstrapped samples.
    idx = np.random.choice(len(data), size=n, replace=True)
    bootstrapped_data = data.iloc[idx].copy()
    bootstrapped_data['ID'] = np.arange(len(bootstrapped_data)) + 1
    bootstrapped_data = bootstrapped_data.reset_index(drop=True)
    
    return bootstrapped_data.copy()



def bootstrap_data_to_gender_proportion(data, proportion_women):

    data = data.copy()

    # Discard members of excess gender randomly.
    num_women = sum(data['Gender'] == 'Female')
    num_men = sum(data['Gender'] == 'Male')
    curr_proportion_women = num_women / (num_women + num_men)
    prop_odds = proportion_women/(1 - proportion_women)

    if curr_proportion_women > proportion_women:
        # Choose diff number of men to bootstrap.
        candidate_gender = 'Male'
        num_to_add = np.round(num_women/prop_odds - num_men).astype(int)
    else:
        # Choose diff number of women to bootstrap.
        candidate_gender = 'Female'
        num_to_add = np.round(num_men*prop_odds - num_women).astype(int)

    candidates = data[data['Gender'] == candidate_gender]['ID'].values
    to_add = np.random.choice(candidates, size=num_to_add, replace=True)
    bootstrapped_data = data.set_index('ID').loc[to_add].reset_index()
    data = pd.concat([data, bootstrapped_data], ignore_index=True)

    return data.copy()


def change_hiring_pool_composition(hiring_data, config):

    hiring_data = hiring_data.copy()
    
    # Filter by demographics.
    if config['department'] is not None:

        # Unpack department.
        prop_women, discipline = config['department']
        hiring_data = hiring_data[hiring_data['STEM'] == discipline].copy()
        hiring_data = bootstrap_data_to_gender_proportion(hiring_data, prop_women).copy()
        if len(hiring_data) == 0:
            raise Exception('Demographics inconsistent with hiring DataFrame.')
        
    return hiring_data.copy()



def get_fixed_and_shuffling_vars(hiring_data, config):

    fixed_vars = [v for v in ALL_HIRING_INTERVENTIONS if not(v in config['hiring_interventions'])]
    fixed_vars = [v if v != 'Age' else 'AgeGroup' for v in fixed_vars]
    shuffling_vars = [v for v in config['hiring_interventions'] if not(v == 'Rate')]
    assert not('Rate' in fixed_vars) and not('Rate' in shuffling_vars)    # breaks everything

    fixed_var_vals = [hiring_data[fv].unique() for fv in fixed_vars]

    return fixed_vars, fixed_var_vals, shuffling_vars


def shuffle_vars(hiring_data, config):
    """
    Make shorter/split.
    """
    # For tests.
    prev_hiring_data = hiring_data.copy()

    # Shuffle variables.
    # Only shuffle if there are demographics (other than Rate) to shuffle.
    if not(config['hiring_interventions'] == ['Rate']):

        fixed_vars, fixed_var_vals, shuffling_vars = get_fixed_and_shuffling_vars(hiring_data, config)

        for curr_fixed_vars in product(*fixed_var_vals):
            if len(curr_fixed_vars) > 0:
                mask = np.logical_and.reduce([hiring_data[fv] == fvv for fv, fvv in zip(fixed_vars, curr_fixed_vars)], axis=0)
            else:
                mask = np.full(len(hiring_data), True)

            data_to_shuffle = hiring_data.loc[mask, shuffling_vars].copy().reset_index(drop=True)
            indices_to_shuffle = data_to_shuffle.index.values.copy()
            assert len(indices_to_shuffle) == len(set(indices_to_shuffle))

            np.random.shuffle(indices_to_shuffle)

            data_to_shuffle = data_to_shuffle.iloc[indices_to_shuffle]
            hiring_data.loc[mask, shuffling_vars] = data_to_shuffle.values

    # Equalising rates.
    if 'Rate' in config['hiring_interventions']:
        hiring_data = bootstrap_data_to_gender_proportion(hiring_data, 0.5).copy()

    # Run basic tests.
    if config['testing']:
        test_shuffle(hiring_data, prev_hiring_data, fixed_vars, shuffling_vars)

    return hiring_data



def test_shuffle(shuffled_data, unshuffled_data, fixed_vars, shuffling_vars):
        
    # No values being created or destroyed.
    for param in ALL_HIRING_INTERVENTIONS:
        new_param, prev_param = shuffled_data[param].values, unshuffled_data[param].values
        assert np.all(np.sort(new_param) == np.sort(prev_param))

    # Fixed values remaining fixed.
    for param in fixed_vars:
        new_param, prev_param = shuffled_data[param].values, unshuffled_data[param].values
        assert np.all(new_param == prev_param)

    # Other columns remaining fixed.
    other_cols = [c for c in shuffled_data.columns if not(c in shuffling_vars)]
    for param in other_cols:
        new_param, prev_param = shuffled_data[param].values, unshuffled_data[param].values
        assert np.all(new_param == prev_param)
