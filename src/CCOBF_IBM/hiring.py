import numpy as np

from CCOBF_IBM.parameters import DATA_COLS
from CCOBF_IBM.bootstrapping import bootstrap_data
from CCOBF_IBM.initial_condition import make_age_groups


def make_hiring_data(data, config):

    hiring_data = data.copy()
    hiring_data = hiring_data.loc[hiring_data.groupby('ID')['InterpYears'].idxmin()]
    hiring_data = make_age_groups(hiring_data, config)
    hiring_data = hiring_data[DATA_COLS + ['AgeGroup']].copy()
    return hiring_data


def get_hiring_model(data, config):
    
    hiring_data = make_hiring_data(data, config)
    return lambda n: bootstrap_data(n, hiring_data.copy(), config)


def run_hiring_event(time, sim_df, hiring_model, attrited, config):

    sim_df = sim_df.copy()

    num_to_hire = np.sum(attrited)
    if num_to_hire > 0:
        new_hires = hiring_model(num_to_hire)
        new_hires['Time'] = time
        new_hires['TimeJoined'] = time
        new_hires['ID'] += sim_df['ID'].max()
        sim_df.loc[attrited, :] = new_hires.to_numpy()

    return sim_df
