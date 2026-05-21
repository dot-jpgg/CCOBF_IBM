
import numpy as np

from CCOBF_IBM.config import PROJECT_ROOT


def df_to_np(df):

    columns = df.columns.values
    numeric_df = df.replace({'Male': 0, 'Female': 1, 'nonEuro': 0, 'Euro': 1, 'nonSTEM': 0, 'STEM': 1})
    arr = numeric_df.values
    return arr.astype(float), columns.tolist()


def post_processing(out):

    numeric_out = []

    for data in out:
        numeric_arr, col_names = df_to_np(data.copy())
        numeric_out.append(numeric_arr)

    return np.array(numeric_out), col_names


def save_output(out, config):

    processed_out = post_processing(out)
    out_arr, col_names = processed_out
    fn = PROJECT_ROOT / 'data' / 'simulated' / config['out_filename']
    np.savez_compressed(fn, out=out_arr, col_names=col_names)
