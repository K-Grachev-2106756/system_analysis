import os
import sys
sys.path.append(os.getcwd())

import numpy as np

from task1.task import parse_json
from task2.task import get_relations_matrix


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


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

    tree = parse_json(os.path.join(parent_dir, "all_data", "tree.json"))
    
    entropy = calc_information_amount(tree)
    
    print("Энтропия:", entropy)

    return entropy


if __name__ == "__main__":
    main()