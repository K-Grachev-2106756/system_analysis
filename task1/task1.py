import json


def parse_json(path: str):
    with open(path, "r") as f:
        data = json.load(f)

    result = []

    queue = [data]
    while len(queue):
        tmp_dict = queue.pop(0)

        for node in tmp_dict:
            queue.append(tmp_dict[node])
            for child in tmp_dict[node]:
                result.append((node, child))

    return result