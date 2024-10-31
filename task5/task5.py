import os
import sys
sys.path.append(os.getcwd())

import numpy as np
import pandas as pd
import json
from collections import Counter


def parse_json(path: str) -> pd.DataFrame:
    with open(path, "r") as f:
        data = json.load(f)

    all_objs = []
    for val in data:
        all_objs.extend(val if isinstance(val, list) else [val])
    all_objs_dict = {v: i for i, v in enumerate(all_objs)}
    
    n_obj = len(all_objs)
    result = np.zeros(shape=(n_obj, n_obj))
    
    used = []
    for part in data:
        indicies = [all_objs_dict[obj] for obj in part] if isinstance(part, list) else [all_objs_dict[part]]
        used.extend(indicies)

        for row in used:
            result[row, indicies] = 1
    
    return pd.DataFrame(result, columns=all_objs)


def prepare_matrices(matrix1: pd.DataFrame, matrix2: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list]:
    cols1, cols2 = matrix1.columns, matrix2.columns

    assert len(set(cols1) - set(cols2)) == 0, "Ранжировки должны содержать одни и те же объекты"

    matrix2 = matrix2[cols1].to_numpy()
    matrix1 = matrix1.to_numpy()

    return matrix1, matrix2, cols1


def calc_contradictions_core(matrix1: np.ndarray, matrix2: np.ndarray, labels: list) -> list:
    rating = np.sum(matrix1 * matrix2, axis=0)

    result, labels = [], np.array(labels)
    for points, obj_count in Counter(rating).items():
        if obj_count > 1:
            indicies = np.where(rating == points)[0]
            result.append(labels[indicies])
    
    return result


if __name__ == "__main__":
    matrix1 = parse_json(os.path.join(os.getcwd(), "task5", "rang1.json"))
    matrix2 = parse_json(os.path.join(os.getcwd(), "task5", "rang2.json"))

    matrix1, matrix2, obj_order = prepare_matrices(matrix1, matrix2)

    print(calc_contradictions_core(matrix1, matrix2, obj_order))