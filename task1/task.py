import os
import sys
sys.path.append(os.getcwd())

import json
from copy import deepcopy

def parse_json(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    result = {}

    queue = [data]
    while len(queue):
        tmp_dict = queue.pop(0)

        for node in tmp_dict:
            queue.append(tmp_dict[node])
            if node not in result:
                result[node] = {"p": [], "c": []}
            for child in tmp_dict[node]:
                if child not in result:
                    result[child] = {"p": [], "c": []}
                result[node]["c"].append(child)
                result[child]["p"].append(node)

    return result


def get_parents(tree, node):
    return deepcopy(tree[node]["p"])


def get_children(tree, node):
    return deepcopy(tree[node]["c"])


def get_brothers(tree, node, exclude_node: bool = True):
    result = set()
    for parent in get_parents(tree, node):
        for brother in get_children(tree, parent):
            result.add(brother)
    
    if exclude_node and (node in result):
        result.remove(node)
    
    return list(result)


def main():
    tree = parse_json("./task1/1.json")

    for i in range(1, 9):
        obj = str(i)
        
        print("Вершина:", obj)
        
        childs = get_children(tree, obj)
        if len(childs):
            print("Дети:", childs)
        else:
            print("Детей нет")
        
        brothers = get_brothers(tree, obj)
        if len(brothers):
            print("Братья:", brothers)
        else:
            print("Братьев нет")            

        print("=" * 10)

if __name__ == "__main__":
    main()