import os
import sys
sys.path.append(os.getcwd())

from task1.task1 import parse_json, get_children, get_parents, get_brothers

# r1 - начальник (0)
# r2 - подчиненный (1)
# r3 - опосредованный начальник (2)
# r4 - опосредованный подчиненный (3)
# r5 - соподчинение на одном уровне (4)

tree = parse_json("./task1/1.json")

result = {}
for node in tree:
    result[node] = [[] for i in range(5)]

    childs = get_children(tree, node)
    result[node][0].extend(childs)

    parents = get_parents(tree, node)
    result[node][1].extend(parents)

    while len(childs):
        for child in get_children(tree, childs.pop(0)):
            childs.append(child)
            result[node][2].append(child)

    while len(parents):
        for parent in get_parents(tree, parents.pop(0)):
            parents.append(parent)
            result[node][3].append(parent)
    
    brothers = get_brothers(tree, node)
    result[node][4].extend(brothers)

    for i in range(5):
        result[node][i] = len(set(result[node][i]))
    result[node][4] = max(result[node][4] - 1, 0)

    print(node, result[node])