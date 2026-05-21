
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


def predict_prob(data, model):

    probs = model.predict(data).values
    assert not np.any(probs < 0)
    return probs


def shuffle_gender(data):

    data = data.copy()
    gender_arr = data['Gender'].values
    np.random.shuffle(gender_arr)
    data['Gender'] = gender_arr
    return data.copy()


def fit_promotion_and_attrition_models(data, config):

    promotion_model = smf.glm(
        formula=config['promotion_formula'], data=data, family=sm.families.Binomial()
    ).fit()
    attrition_model = smf.glm(
        formula=config['attrition_formula'], data=data, family=sm.families.Binomial()
    ).fit()

    return promotion_model, attrition_model


def run_promotion_event(sim_df, promotion_model, config):

    # Implement interventions.
    if config['promotion_interventions']:
        sim_df = shuffle_gender(sim_df.copy())  # don't modify original

    p_promotion = predict_prob(sim_df, promotion_model)
    professor = sim_df['CurrRank'] == 4
    promoted = np.random.random(len(sim_df)) < p_promotion
    promoted = promoted & ~professor    # Professors can't be promoted.
    return promoted


def run_attrition_event(sim_df, attrition_model, config):

    # Implement interventions.
    if config['attrition_interventions']:
        sim_df = shuffle_gender(sim_df.copy())  # don't modify original

    p_attrition = predict_prob(sim_df, attrition_model)
    attrited = np.random.random(len(sim_df)) < p_attrition
    too_old = sim_df['Age'] > config['max_age']
    attrited[too_old] = 1
    return attrited