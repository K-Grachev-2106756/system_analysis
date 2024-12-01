import os 
import sys
import json
from typing import Optional

import pandas as pd
import numpy as np


sys.path.append(os.getcwd())


def gen_dice_table() -> np.ndarray:
    index = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    columns = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36]

    df = pd.DataFrame(0, index=index, columns=columns)

    for i in range(1, 7):
        for j in range(1, 7):
            sm = i + j
            mlt = i * j

            df.at[sm, mlt] += 1

    return df.to_numpy()


def parse_json(path: Optional[str] = None) -> list:
    if path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        path = os.path.join(parent_dir, "all_data", "table.json")
    
    with open(path, "r") as f:
        return json.load(f)
    

def calc_entropy(probs: np.ndarray) -> float:
    tmp_probs = probs[probs != 0]

    return -(tmp_probs * np.log2(tmp_probs)).sum()


def main() -> list:
    table = np.array(parse_json())

    probs_table = table / table.sum()
    entropy_total = calc_entropy(probs_table)

    probs_x = probs_table.sum(axis=0)
    entropy_x = calc_entropy(probs_x)

    probs_y = probs_table.sum(axis=1)
    entropy_y = calc_entropy(probs_y)

    entropy_y_cond_x =  sum(
        [probs_y[i] * calc_entropy(probs_table[i] / probs_y[i]) for i in range(len(table))]
    )

    inf_in_x_about_y = entropy_x - entropy_y_cond_x

    result = [entropy_total, entropy_y, entropy_x, entropy_y_cond_x, inf_in_x_about_y]
    result = [round(v, 2) for v in result]

    for i, message in enumerate([
        "энтропия двух связанных (совместных) событий",
        "энтропия события А",
        "энтропия события B",
        "условная энтропия события B связанного с событием A",
        "информация в событии A о событии B",
    ]):
        print(f"{message}: {result[i]}")

    return result


if __name__ == "__main__":
    main()
