from tqdm import tqdm

from CCOBF_IBM.initial_condition import get_initial_condition
from CCOBF_IBM.promotion_and_attrition import fit_promotion_and_attrition_models, run_promotion_event, run_attrition_event
from CCOBF_IBM.hiring import run_hiring_event, get_hiring_model


def run_year(time, sim_df, promotion_model, attrition_model, hiring_model, config):

    sim_df = sim_df.copy()

    # Promotion.
    promoted = run_promotion_event(sim_df, promotion_model, config)

    # Promotion.
    sim_df.loc[promoted, 'CurrRank'] += 1
    sim_df.loc[promoted, 'TimeSpentAtRank'] = 0

    # Increment time-based vars.
    sim_df['Age'] += 1
    sim_df['TimeSpentAtRank'] += 1
    sim_df['RetirementAge'] = (sim_df['Age'] >= 65).astype(int)

    # Add new hires and remove attrited individuals.
    # NOTE: individuals are removed during the hiring event;
    # the attrition event CHOOSES individuals to leave, but
    # doesn't actually remove them.
    attrited = run_attrition_event(sim_df, attrition_model, config)
    sim_df = run_hiring_event(time, sim_df, hiring_model, attrited, config)

    return sim_df.copy()


def initialise(data, config):

    # Initialise.
    init_df = get_initial_condition(data, config).copy()
    out = [init_df.copy()]
    times = list(range(1, config['num_years'])) # list wrapper for tqdm
    return init_df, out, times


def fit_models(data, config):

    # Fit promotion, attrition, and hiring models.
    promotion_model, attrition_model = fit_promotion_and_attrition_models(data, config)
    hiring_model = get_hiring_model(data.copy(), config)

    return promotion_model, attrition_model, hiring_model


def simulate(data, config):

    # Initialise and fit sub-models.
    init_df, out, times = initialise(data, config)
    sim_df = init_df.copy()
    promotion_model, attrition_model, hiring_model = fit_models(data, config)

    # Run model.
    for time in tqdm(times, desc='Running IBM...'):
        sim_df['Time'] = time
        sim_df = run_year(
            time, sim_df,
            promotion_model, attrition_model, hiring_model,
            config
        ).copy()
        out.append(sim_df.copy())

    return out