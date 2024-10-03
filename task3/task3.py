import os
import sys
sys.path.append(os.getcwd())

import numpy as np

from task1.task1 import parse_json
from task2.task2 import get_relations_matrix


def calc_information_amount(tree):
    matrix = get_relations_matrix(tree)

    max_rel = matrix.shape[0] - 1

    information_amount = 0
    for node in matrix:
        H_i = 0
        for rel in node: 
            if rel != 0:
                P_ij = rel / max_rel
                H_i += P_ij * np.log2(P_ij)
        
        information_amount += -H_i

    return round(information_amount, 2)


if __name__ == "__main__":
    tree = parse_json("./task1/1.json")

    print(calc_information_amount(tree))