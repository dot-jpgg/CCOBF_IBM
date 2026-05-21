DEFAULT_CONFIG = {
    'num_years':                500,
    'department_size':          100,
    'seed':                     123,
    'min_age':                  25,
    'max_age':                  75,
    'age_group_size':           5,
    'promotion_interventions':  None,   # ['Gender'], or None
    'attrition_interventions':  None,   # ['Gender'], or None
    'hiring_interventions':     None,   # Choose from ['Rate', 'Age', 'CurrRank', 'STEM'], or None
    'department':               None,   # (prop_women, discipline), or None
    'testing':                  False
}

def build_config(**kwargs):
    config = DEFAULT_CONFIG.copy()
    config.update(kwargs)
    return config

ALL_HIRING_INTERVENTIONS = ['Age', 'CurrRank', 'STEM']
DATA_COLS = ['ID', 'Age', 'TimeSpentAtRank', 'CurrRank', 'Gender', 'STEM', 'RetirementAge']
OUT_COLS = DATA_COLS + ['Time', 'TimeJoined']   # added during simulation

RANKS = [1, 2, 3, 4]

# Output indices.
ID = 0
AGE = 1
TSAR = 2
RANK = 3
GENDER = 4
STEM = 5
RETIREMENT_AGE = 6
TIME = 7
TIME_JOINED = 8