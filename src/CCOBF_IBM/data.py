import pandas as pd

from CCOBF_IBM.config import PROJECT_ROOT

# Example data generated using ChatGPT-5. See GitHub README for details.
TOY_DATA = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'toy_academic_careers_dataset.csv')