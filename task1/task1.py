import json


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
    return tree[node]["p"]


def get_children(tree, node):
    return tree[node]["c"]


def get_brothers(tree, node):
    result = []
    for parent in get_parents(tree, node):
        for brother in get_children(tree, parent):
            result.append(brother)
    
    # if node in result:
    #     result.remove(node)
    
    return result


if __name__ == "__main__":
    tree = parse_json("./task1/1.json")

    print(get_children(tree, "3"))
    print(get_brothers(tree, "3"))